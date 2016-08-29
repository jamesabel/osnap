
import argparse

import osnap.osnapy_win
import osnap.osnapy_mac
import osnap.util
import osnap.const
import osnap.write_timestamp


def create_osnapy(version, clean_cache=False, verbose=False):
    if verbose:
        print('creating osnapy Python environment using python %s' % version)
    if osnap.util.is_windows():
        osnap.osnapy_win.create_python_win(version, clean_cache, verbose)
    elif osnap.util.is_mac():
        osnap.osnapy_mac.create_python_mac(version, clean_cache, verbose)
    else:
        raise NotImplementedError
    add_packages_from_requirements_file(verbose=verbose)


def add_packages_from_requirements_file(requirements_file_path='requirements.txt', verbose=False):
    with open(requirements_file_path) as f:
        for l in f:
            package = l.strip()
            if len(l) > 0:
                if verbose:
                    print('adding %s to python environment' % str(package))
                if osnap.util.is_windows():
                    osnap.osnapy_win.add_package_win(package, verbose)
                elif osnap.util.is_mac():
                    osnap.osnapy_mac.add_package_mac(package, verbose)
                else:
                    raise NotImplementedError


def main():
    parser = argparse.ArgumentParser(description='create the osnapy Python environment',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-p', '--python', default='3.5', help='python version')
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='print more verbose messages')
    args = parser.parse_args()
    create_osnapy(args.python, args.verbose)

if __name__ == '__main__':
    main()
