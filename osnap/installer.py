
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
import osnap.make_nsis
import osnap.make_pkgproj


def copy_app(destination_directory, application_dir, verbose):
    for d in [application_dir, osnap.const.python_folder]:
        if verbose:
            print('copying %s to %s' % (d, os.path.join(destination_directory, d)))
        distutils.dir_util.copy_tree(d, os.path.join(destination_directory, d))
    for f in ['main.py']:
        if verbose:
            print('copying %s to %s' % (f, destination_directory))
        shutil.copy2(f, destination_directory)


def _mac_os_dir(application_name):
    return os.path.join(osnap.const.dist_dir, application_name + '.app', 'Contents', 'MacOS')


def unzip_launcher(dist_dir, verbose):
    launch_zip_path = os.path.join(os.path.dirname(sys.executable), '..', osnap.const.package_name,
                                   osnap.util.get_launch_name() + '.zip')
    if not os.path.exists(launch_zip_path):
        print('error: can not find %s' % launch_zip_path)
        return
    if verbose:
        print('unzipping %s to %s' % (launch_zip_path, dist_dir))
    zip_ref = zipfile.ZipFile(launch_zip_path, 'r')
    zip_ref.extractall(dist_dir)
    zip_ref.close()


def make_installer(author, application_name, description='', url='', project_packages=[], version='0.0.0',
                   compile_code=False, verbose=False):

    print('clearing and making %s (%s)' % (osnap.const.dist_dir, os.path.abspath(osnap.const.dist_dir)))
    osnap.util.rm_mk_tree(osnap.const.dist_dir)
    print('done making %s (%s)' % (osnap.const.dist_dir, os.path.abspath(osnap.const.dist_dir)))

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

    unzip_launcher(osnap.const.dist_dir, verbose)
    if osnap.util.is_mac():
        macos_dir = _mac_os_dir(application_name)
        os.rename(os.path.join(osnap.const.dist_dir, 'launch.app'),
                  os.path.join(osnap.const.dist_dir, application_name + '.app'))
        copy_app(macos_dir, application_name, verbose)
        for project_package in project_packages:
            if project_package != application_name:
                dest = os.path.join(macos_dir, project_package)
                if verbose:
                    print('copying %s to %s' % (project_package, dest))
                distutils.dir_util.copy_tree(project_package, dest)
        os.chmod(os.path.join(macos_dir, 'launch'), 0o777)

        # make dmg
        dmg_command = ['hdiutil', 'create', '-volname', application_name, '-srcfolder', os.path.abspath('dist'), '-ov',
                       '-format', 'UDZO', application_name + '.dmg']
        dmg_command = ' '.join(dmg_command)
        if verbose:
            print('%s' % str(dmg_command))
        subprocess.check_call(dmg_command, shell=True)

        # make pkg based installer
        pkgproj_path = application_name + '.pkgproj'
        pkgproj_command = [os.path.join(os.sep, 'usr', 'local', 'bin', 'packagesbuild'), pkgproj_path]
        osnap.make_pkgproj.make_prkproj(application_name, pkgproj_path, verbose)
        pkgproj_command = ' '.join(pkgproj_command)
        if verbose:
            print('%s' % str(pkgproj_command))
        subprocess.check_call(pkgproj_command, shell=True)

    elif osnap.util.is_windows():

        copy_app(os.path.join(osnap.const.dist_dir, osnap.const.windows_app_dir), application_name, verbose)

        # application .exe
        exe_name = application_name + '.exe'
        orig_launch_exe_path = os.path.join(osnap.const.dist_dir, 'launch.exe')
        dist_exe_path = os.path.join(osnap.const.dist_dir, exe_name)
        if verbose:
            print('moving %s to %s' % (orig_launch_exe_path, dist_exe_path))
        os.rename(orig_launch_exe_path, dist_exe_path)

        # support files
        for f in [application_name + '.ico', 'LICENSE']:
            shutil.copy2(f, osnap.const.dist_dir)

        # write NSIS script
        nsis_file_name = application_name + '.nsis'

        nsis_defines = collections.OrderedDict()
        nsis_defines['COMPANYNAME'] = author
        nsis_defines['APPNAME'] = application_name
        nsis_defines['EXENAME'] = exe_name
        nsis_defines['DESCRIPTION'] = '"' + description + '"'  # the description must be in quotes

        v = version.split('.')
        nsis_defines['VERSIONMAJOR'] = v[0]
        nsis_defines['VERSIONMINOR'] = v[1]
        nsis_defines['VERSIONBUILD'] = v[2]

        # These will be displayed by the "Click here for support information" link in "Add/Remove Programs"
        # It is possible to use "mailto:" links in here to open the email client
        nsis_defines['HELPURL'] = url  # "Support Information" link
        nsis_defines['UPDATEURL'] = url  # "Product Updates" link
        nsis_defines['ABOUTURL'] = url  # "Publisher" link

        if verbose:
            print('writing %s' % nsis_file_name)
        nsis = osnap.make_nsis.MakeNSIS(nsis_defines, nsis_file_name, project_packages)
        nsis.write_all()

        shutil.copy(nsis_file_name, osnap.const.dist_dir)

        os.chdir(osnap.const.dist_dir)

        pkgproj_command = [os.path.join('c:', os.sep, 'Program Files (x86)', 'NSIS', 'makensis'), nsis_file_name]
        if verbose:
            print('%s' % str(pkgproj_command))
        subprocess.check_call(pkgproj_command)
    else:
        raise NotImplementedError


def main():
    parser = argparse.ArgumentParser(description='create the osnap installer',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--author', required=True, help='name of author, e.g. a person or a company')
    parser.add_argument('--app', required=True, help='application name')
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='print more verbose messages')
    args = parser.parse_args()
    make_installer(args.author, args.app, verbose=args.verbose)

if __name__ == '__main__':
    main()