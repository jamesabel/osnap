
import fnmatch
import py_compile
import os
import shutil
import distutils.dir_util
import sys
import datetime
import subprocess
import collections
import zipfile
import argparse

import osnap.util
import osnap.util
import osnap.const
import osnap.write_timestamp
import osnap.make_nsis


def copy_app(destination_directory, verbose):
    # todo: get 'application' programmatically
    for d in ['application', osnap.const.python_folder]:
        if verbose:
            print('copying %s to %s' % (d, os.path.join(destination_directory, d)))
        distutils.dir_util.copy_tree(d, os.path.join(destination_directory, d))
    for f in ['main.py']:
        if verbose:
            print('copying %s to %s' % (f, destination_directory))
        shutil.copy2(f, destination_directory)


def unzip_launcher(dist_dir, verbose):
    launch_zip_path = os.path.join(os.path.dirname(sys.executable), '..', 'osnap',
                                   osnap.util.get_launch_name() + '.zip')
    if not os.path.exists(launch_zip_path):
        print('error: can not find %s' % launch_zip_path)
        return
    if verbose:
        print('unzipping %s to %s' % (launch_zip_path, dist_dir))
    zip_ref = zipfile.ZipFile(launch_zip_path, 'r')
    zip_ref.extractall(dist_dir)
    zip_ref.close()


def create_installer(author, application_name, description='', url='', project_packages=[], compile_code=False,
                     verbose=False):

    osnap.write_timestamp.write_timestamp()

    dist_dir = 'dist'
    osnap.util.rm_mk_tree(dist_dir)

    # If the user has been using osnap's python, you shouldn't have to compile the code here, which keeps the
    # distribution size smaller.  However, just in case the installed program is having an issue with non-compiled
    # code (e.g. it's been installed into a read-only area), we have this option.
    if compile_code:
        if verbose:
            print('compiling')
        for root, dirnames, filenames in os.walk(osnap.const.python_folder):
            for filename in fnmatch.filter(filenames, '*.py'):
                path = os.path.join(root, filename)
                # special case: don't compile Python 2 code from PyQt
                if 'port_v2' not in path:
                    py_compile.compile(path)

    unzip_launcher(dist_dir, verbose)
    if osnap.util.is_mac():
        macos_dir = os.path.join(dist_dir, 'launch.app', 'Contents', 'MacOS')
        copy_app(macos_dir, verbose)
        os.chmod(os.path.join(macos_dir, 'launch'), 0o555)
    elif osnap.util.is_windows():

        # todo: get 'osnapp' programmatically
        copy_app(os.path.join(dist_dir, 'osnapp'), verbose)

        # application .exe
        exe_name = application_name + '.exe'
        orig_launch_exe_path = os.path.join(dist_dir, 'launch.exe')
        dist_exe_path = os.path.join(dist_dir, exe_name)
        if verbose:
            print('moving %s to %s' % (orig_launch_exe_path, dist_exe_path))
        os.rename(orig_launch_exe_path, dist_exe_path)

        # support files
        for f in [application_name + '.ico', 'LICENSE']:
            shutil.copy2(f, dist_dir)

        # write NSIS script
        nsis_file_name = application_name + '.nsis'

        nsis_defines = collections.OrderedDict()
        nsis_defines['COMPANYNAME'] = author
        nsis_defines['APPNAME'] = application_name
        nsis_defines['EXENAME'] = exe_name
        nsis_defines['DESCRIPTION'] = '"' + description + '"'  # the description must be in quotes

        import _build_

        s = int(_build_.seconds_since_epoch)
        dt = datetime.datetime.fromtimestamp(s)
        nsis_defines['VERSIONMAJOR'] = dt.year
        nsis_defines['VERSIONMINOR'] = dt.timetuple().tm_yday
        nsis_defines['VERSIONBUILD'] = _build_.version

        # These will be displayed by the "Click here for support information" link in "Add/Remove Programs"
        # It is possible to use "mailto:" links in here to open the email client
        nsis_defines['HELPURL'] = url  # "Support Information" link
        nsis_defines['UPDATEURL'] = url  # "Product Updates" link
        nsis_defines['ABOUTURL'] = url  # "Publisher" link

        if verbose:
            print('writing %s' % nsis_file_name)
        nsis = osnap.make_nsis.MakeNSIS(nsis_defines, nsis_file_name, project_packages)
        nsis.write_all()

        shutil.copy(nsis_file_name, dist_dir)

        os.chdir(dist_dir)

        command = [os.path.join('c:', os.sep, 'Program Files (x86)', 'NSIS', 'makensis'), nsis_file_name]
        if verbose:
            print('%s' % str(command))
        subprocess.check_call(command)
    else:
        raise NotImplementedError


def main():
    parser = argparse.ArgumentParser(description='create the osnapy Python environment',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--author', required=True, help='name of author, e.g. a person or a company')
    parser.add_argument('--app', required=True, help='application name')
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='print more verbose messages')
    args = parser.parse_args()
    create_installer(args.author, args.app, verbose=args.verbose)

if __name__ == '__main__':
    main()