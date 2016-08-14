
import bz2
import base64
import shutil
import os

import osnap.osnapy_win
import osnap.osnapy_mac
import osnap.util
import osnap.const
import osnap.write_timestamp
import osnap.launchwin
import osnap.launchmac


def create_osnapy(version, clean_cache=False, verbose=False):
    if verbose:
        print('creating osnapy')
    if osnap.util.is_windows():
        osnap.osnapy_win.create_python_win(version, clean_cache, verbose)
    elif osnap.util.is_mac():
        osnap.osnapy_mac.create_python_mac(version, clean_cache, verbose)
    else:
        raise NotImplementedError


# todo: add an optional version
def add_package(package, verbose=False):
    if verbose:
        print('adding %s to python environment' % str(package))
    if osnap.util.is_windows():
        osnap.osnapy_win.add_package_win(package, verbose)
    elif osnap.util.is_mac():
        osnap.osnapy_mac.add_package_mac(package, verbose)
    else:
        raise NotImplementedError


def add_packages_from_requirements_file(requirements_file_path, verbose=False):
    with open(requirements_file_path) as f:
        for l in f:
            l = l.strip()
            if len(l) > 0:
                add_package(l, verbose=verbose)


def unpack_launcher(verbose=False):
    zip_file = osnap.util.get_launch_name() + '.zip'
    launch_name = osnap.util.get_launch_name()

    if os.path.exists(launch_name):
        if verbose:
            print('removing directory : %s' % launch_name)
        shutil.rmtree(launch_name)

    if verbose:
        print('unpacking %s' % launch_name)
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
    if verbose:
        print('making %s executable' % launch_name)
    mod = 0o755
    for root, dirs, files in os.walk(launch_name):
        for dir in dirs:
            os.chmod(os.path.join(root, dir), mod)
        for f in files:
            os.chmod(os.path.join(root, f), mod)

    if verbose:
        print('cleanup : removing %s' % zip_file)
    os.remove(zip_file)
