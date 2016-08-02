
import fnmatch
import py_compile
import os
import shutil
import distutils.dir_util
import time
import osnap.util

if osnap.util.is_windows():
    import osnap.installer_win
import osnap.util
import osnap.const
import osnap.write_timestamp


def create_installer(author, application_name, description='', url='', project_packages=[], compile_code=False,
                     verbose=False):

    osnap.write_timestamp.write_timestamp()

    dist_dir = 'dist'
    # fancy rmtree, since for some reason shutil.rmtree can return before the tree is actually removed
    count = 0
    while os.path.exists(dist_dir) and count < 100:
        try:
            shutil.rmtree(dist_dir)
        except FileNotFoundError:
            pass
        except IOError:
            time.sleep(1)
        count += 1
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

    if osnap.util.is_mac():
        macos_dir = os.path.join(dist_dir, 'launch.app', 'Contents', 'MacOS')
        for d in ['application', osnap.const.python_folder]:
            # todo: get launch.app from somewhere programmatic
            distutils.dir_util.copy_tree(d, os.path.join(macos_dir, d))
        distutils.dir_util.copy_tree(os.path.join(osnap.util.get_launch_name()), dist_dir)
        for f in ['main.py']:
            shutil.copy2(f, macos_dir)
    elif osnap.util.is_windows():
        raise NotImplementedError

