
import argparse
import logging

import osnap.osnapy_win
import osnap.osnapy_mac
import osnap.osnapy_mac_pyrun
import osnap.util
import osnap.const
import osnap.check_version

LOGGER = logging.getLogger('osnapy')

def make_osnapy(
        python_version,
        application_name        = None,
        clean_cache             = False,
        use_pyrun               = False,
        force_app_uninstall     = False,
        architecture            = '64bit',
        ):

    osnap.check_version.check_version('osnapy')

    LOGGER.debug('creating osnapy Python environment using python %s' % python_version)
    if osnap.util.is_mac() and application_name is None:
        raise Exception('must specify the application name on mac')
    if osnap.util.is_windows():
        osnapy = osnap.osnapy_win.OsnapyWin(python_version, application_name, clean_cache, architecture=architecture)
    elif osnap.util.is_mac():
        if use_pyrun:
            osnapy = osnap.osnapy_mac_pyrun.OsnapyMacPyrun(python_version, application_name, clean_cache)
        else:
            osnapy = osnap.osnapy_mac.OsnapyMac(python_version, application_name, clean_cache, force_app_uninstall)
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
    parser.add_argument('-A', '--architecture', default='64bit', choices=['64bit', '32bit'], help='The architecture to use for the launcher')
    parser.add_argument('-p', '--python_version', default=osnap.const.default_python_version, help='python version')
    parser.add_argument('-c', '--clear', action='store_true', default=False, help='clear cache')
    parser.add_argument('-e', '--egenix_pyrun', action='store_true', default=False, help='use eGenix™ PyRun™')
    parser.add_argument('-f', '--force_uninstall', action='store_true', default=False,
                        help='force application uninstalls if necessary')
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='print more verbose messages')

    args = parser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
        logging.getLogger().debug("Verbose mode on")
    else:
        logging.basicConfig(level=logging.INFO)
    make_osnapy(
        python_version      = args.python_version,
        application_name    = args.application,
        clean_cache         = args.clear,
        use_pyrun           = args.egenix_pyrun,
        force_app_uninstall = args.force_uninstall,
        architecture        = args.architecture
    )

if __name__ == '__main__':
    main()
