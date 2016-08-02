
import fnmatch
import py_compile
import os
import shutil
import distutils.dir_util

import osnap.util

if osnap.util.is_windows():
    import osnap.installer_win
if osnap.util.is_mac():
    import osnap.installer_mac
import osnap.util
import osnap.const
import osnap.write_timestamp


def create_installer(author, application_name, description='', url='', project_packages=[], compile_code=False,
                     verbose=False):

    osnap.write_timestamp.write_timestamp()

    # copy over launcher
    dist_dir = 'dist'
    try:
        shutil.rmtree(dist_dir)
    except FileNotFoundError:
        pass
    os.mkdir(dist_dir)

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

    for d in ['application', osnap.const.python_folder]:
        distutils.dir_util.copy_tree(d, os.path.join(dist_dir, d))
    distutils.dir_util.copy_tree(os.path.join(osnap.util.get_launch_name()), dist_dir)
    for f in ['main.py']:
        shutil.copy2(f, dist_dir)

    print('stopped here')
    return

    if osnap.util.is_windows():
        osnap.installer_win.create_installer_win(author, application_name, description, url, project_packages, verbose)
    elif osnap.util.is_mac():
        osnap.installer_mac.create_installer_mac(author, application_name, description, url, project_packages, verbose)
    else:
        raise NotImplementedError
