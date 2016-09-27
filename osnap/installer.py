
import argparse

import osnap.const
import osnap.util
import osnap.installer_mac
import osnap.installer_win


def make_installer(python_version, application_name, author='', description='', url='', compile_code=True,
                   verbose=False, use_pyrun=False):
    if osnap.util.is_mac():
        installer = osnap.installer_mac.OsnapInstallerMac(python_version, application_name, author, description, url,
                                                          compile_code, verbose, use_pyrun)
    elif osnap.util.is_windows():
        installer = osnap.installer_win.OsnapInstallerWin(python_version, application_name, author, description, url,
                                                          compile_code, verbose)
    else:
        raise NotImplementedError

    installer.make_installer()


def main():
    parser = argparse.ArgumentParser(description='create the osnap installer',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-a', '--application', default=None, help='application name (required for OSX/MacOS)')
    parser.add_argument('-p', '--python_version', default=osnap.const.default_python_version, help='python version')
    parser.add_argument('-e', '--egenix_pyrun', action='store_true', default=False, help='use eGenix™ PyRun™')
    parser.add_argument('-n', '--name_of_author', default='', help='author name')
    parser.add_argument('-d', '--description', default='', help='application description')
    parser.add_argument('-u', '--url', default='', help='application URL')
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='print more verbose messages')
    args = parser.parse_args()

    make_installer(args.python_version, args.application, args.name_of_author, args.description, args.url,
                   True, args.verbose, args.egenix_pyrun)

if __name__ == '__main__':
    main()
