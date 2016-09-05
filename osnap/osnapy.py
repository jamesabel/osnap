
import argparse
import subprocess
import os

import osnap.osnapy_win
import osnap.osnapy_mac
import osnap.util
import osnap.const
import osnap.write_timestamp
import osnap.source_paths


def make_osnapy(version, clean_cache=False, verbose=False):
    if verbose:
        print('creating osnapy Python environment using python %s' % version)
    if osnap.util.is_windows():
        osnap.osnapy_win.create_python_win(version, clean_cache, verbose)
    elif osnap.util.is_mac():
        osnap.osnapy_mac.create_python_mac(version, clean_cache, verbose)
    else:
        raise NotImplementedError
    add_packages_from_requirements_file(verbose=verbose)


def add_packages_from_requirements_file(requirements_file_path='requirements.txt', package_source_paths={},
                                        verbose=False):

    # requirements_file_path: path to requirements file
    # package_source_paths: a dict where the key is the package name and the value is the URL to the source .zip

    with open(requirements_file_path) as f:
        for l in f:
            package = l.strip()
            if len(l) > 0:
                ret = None
                if verbose:
                    print('adding %s to python environment' % str(package))
                if osnap.util.is_windows():
                    ret = osnap.osnapy_win.add_package_win(package, verbose)
                elif osnap.util.is_mac():
                    if package == 'cryptography':

                        # pycparser is particularly problematic - we have to install it from source before we
                        # attempt to install cryptography
                        _p = 'pycparser'
                        _install_from_source(_p, osnap.source_paths.source_paths[_p], verbose)

                    ret = osnap.osnapy_mac.add_package_mac(package, verbose)
                else:
                    raise NotImplementedError
                if ret != 0:
                    print('%s install failed - attempting to install from source' % package)
                    if package in package_source_paths:
                        _install_from_source(package, package_source_paths[package], verbose)
                    else:
                        if package in osnap.source_paths.source_paths:
                            _install_from_source(package, osnap.source_paths.source_paths[package], verbose)


def _install_from_source(package_name, url, verbose):
    msg = 'installing %s from source' % package_name
    print('start : %s' % msg)
    if url[-10:] == 'master.zip':
        source_file = package_name + '.zip'
        d = os.path.abspath(os.path.join(osnap.const.TEMP_FOLDER, package_name, package_name + '-master'))
    else:
        source_file = url[url.rfind('/')+1:]
        d = os.path.abspath(os.path.join(osnap.const.TEMP_FOLDER, package_name, source_file.replace('.tar.gz', '')))
    osnap.util.get(url, osnap.const.CACHE_FOLDER, source_file, verbose)
    osnap.util.extract(osnap.const.CACHE_FOLDER, source_file,
                       os.path.join(osnap.const.TEMP_FOLDER, package_name), verbose)
    cmd = os.path.abspath(os.path.join(osnap.const.python_folder, 'bin', 'python3')) + ' setup.py install'
    print(cmd)
    print(d)
    subprocess.run(cmd, env=osnap.const.ENV, cwd=d, shell=True)
    if verbose:
        print('done : %s' % msg)


def main():
    if osnap.util.is_mac():
        default_python = '3.5'
    elif osnap.util.is_windows():
        default_python = '3.5.2'
    else:
        default_python = None
        print('platform not supported')
    parser = argparse.ArgumentParser(description='create the osnapy Python environment',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-p', '--python', default=default_python, help='python version')
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='print more verbose messages')
    args = parser.parse_args()
    if args.verbose:
        print('verbose on')
    make_osnapy(args.python, args.verbose)

if __name__ == '__main__':
    main()
