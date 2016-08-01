
import bz2
import base64
import shutil
import os

import osnap.util

import osnap.python_environment_win
import osnap.python_environment_mac
import osnap.util
import osnap.const
import osnap.write_timestamp
import osnap.launchwin
import osnap.launchmac


def create_python(version, clean_cache=False, verbose=False):
    if verbose:
        print('creating python environment')
    if osnap.util.is_windows():
        osnap.python_environment_win.create_python_win(version, clean_cache, verbose)
    elif osnap.util.is_mac():
        osnap.python_environment_mac.create_python_mac(version, clean_cache, verbose)
    else:
        raise NotImplementedError


def add_packages(requirements, verbose=False):
    if verbose:
        print('adding %s to python environment' % str(requirements))
    if osnap.util.is_windows():
        osnap.python_environment_win.add_packages_win(requirements, verbose)
    elif osnap.util.is_mac():
        osnap.python_environment_mac.add_packages_mac(requirements, verbose)
    else:
        raise NotImplementedError


def unpack_launcher(verbose=False):
    if verbose:
        print('unpacking launcher')
    zip_file = osnap.util.get_launch_name() + '.zip'
    launch_name = osnap.util.get_launch_name()

    with open(zip_file, 'wb') as out_file:
        if osnap.util.is_windows():
            launch_code = osnap.launchwin.launchwin
        elif osnap.util.is_mac():
            launch_code = osnap.launchmac.launchmac
        else:
            raise NotImplementedError
        out_file.write(bz2.decompress(base64.b16decode(launch_code)))
    shutil.unpack_archive(zip_file, launch_name)

    # make launcher executable
    mod = 0o755
    for root, dirs, files in os.walk(launch_name):
        for dir in dirs:
            os.chmod(os.path.join(root, dir), mod)
        for f in files:
            os.chmod(os.path.join(root, f), mod)
    os.remove(zip_file)
