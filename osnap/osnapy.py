
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


def _install_from_source(package_name, zip_url, verbose):
    msg = 'installing %s from source' % package_name
    if verbose:
        print('start : %s' % msg)
    pycparser_zip_file = package_name + '.zip'
    pycparser_dir = os.path.abspath(os.path.join(osnap.const.TEMP_FOLDER, package_name, package_name + '-master'))
    osnap.util.get(zip_url, osnap.const.CACHE_FOLDER, pycparser_zip_file, verbose)
    osnap.util.extract(osnap.const.CACHE_FOLDER, pycparser_zip_file,
                       os.path.join(osnap.const.TEMP_FOLDER, package_name), verbose)
    cmd = os.path.abspath(os.path.join(osnap.const.python_folder, 'bin', 'python3')) + ' setup.py install'
    if verbose:
        print(cmd)
        print(pycparser_dir)
    subprocess.run(cmd, shell=True, env=osnap.const.ENV, cwd=pycparser_dir)
    if verbose:
        print('done : %s' % msg)


def main():
    parser = argparse.ArgumentParser(description='create the osnapy Python environment',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-p', '--python', default='3.5', help='python version')
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='print more verbose messages')
    args = parser.parse_args()
    make_osnapy(args.python, args.verbose)

if __name__ == '__main__':
    main()
