
import argparse

import osnap.osnapy_win
import osnap.osnapy_mac
import osnap.osnapy_mac_pyrun
import osnap.util
import osnap.const


def make_osnapy(python_version, application_name=None, clean_cache=False, verbose=False, use_pyrun=False,
                force_app_uninstall=False):
    if osnap.util.is_mac() and application_name is None:
        s = 'error : must specify the application name - use -h for help'
        print(s)
        exit(s)
    if verbose:
        print('creating osnapy Python environment using python %s' % python_version)
    if osnap.util.is_windows():
        osnapy = osnap.osnapy_win.OsnapyWin(python_version, application_name, clean_cache, verbose=verbose)
    elif osnap.util.is_mac():
        if use_pyrun:
            osnapy = osnap.osnapy_mac_pyrun.OsnapyMacPyrun(python_version, application_name, clean_cache,
                                                           verbose=verbose)
        else:
            osnapy = osnap.osnapy_mac.OsnapyMac(python_version, application_name, clean_cache, force_app_uninstall,
                                                verbose)
    else:
        raise NotImplementedError
    osnapy.create_python()
    osnapy.pip('pip')
    osnapy.pip('setuptools')
    osnapy.pip(None)  # install all from requirements.txt


def main():

    parser = argparse.ArgumentParser(description='create the osnapy Python environment',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-a', '--application', default=None, help='application name (required for OSX/MacOS)')
    parser.add_argument('-p', '--python_version', default=osnap.const.default_python_version, help='python version')
    parser.add_argument('-c', '--clear', action='store_true', default=False, help='clear cache')
    parser.add_argument('-e', '--egenix_pyrun', action='store_true', default=False, help='use eGenix™ PyRun™')
    parser.add_argument('-f', '--force_uninstall', action='store_true', default=False,
                        help='force application uninstalls if necessary')
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='print more verbose messages')

    args = parser.parse_args()
    if args.verbose:
        print('verbose on')
    make_osnapy(args.python_version, args.application, args.clear, args.verbose, args.egenix_pyrun, args.force_uninstall)

if __name__ == '__main__':
    main()
