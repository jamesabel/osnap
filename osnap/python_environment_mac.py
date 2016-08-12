import os
import subprocess
import shutil
import glob
import bz2
import base64


import osnap.make_nsis
import osnap.write_timestamp
import osnap.const
import osnap.util


def write_launcher_mac(file_name, verbose):
    pass


def create_python_mac(version, clean_cache, verbose):
    """
    Create a full, stand-alone python installation with the required packages
    """

    cache_folder = 'cache'

    osnap.util.make_dir(osnap.const.python_folder, True, verbose)
    osnap.util.make_dir(cache_folder, clean_cache, verbose)

    # get the embeddable Python .zip
    # version here is x.y (e.g. 3.5), not z.y.z (e.g. not 3.5.2)

    # version 2.2.1 produces a "Segmentation fault: 11" error when python is run:
    # zip_file = 'egenix-pyrun-2.2.1-py%s_ucs4-macosx-10.5-x86_64.tgz' % version
    # so use a prior version:
    zip_file = 'egenix-pyrun-2.2.0-py%s_ucs4-macosx-10.5-x86_64.tgz' % version

    zip_url = 'https://downloads.egenix.com/python/%s' % zip_file
    osnap.util.get(zip_url, cache_folder, zip_file, verbose)
    osnap.util.extract(cache_folder, zip_file, osnap.const.python_folder, verbose)

    python_path = os.path.join(osnap.const.python_folder, 'bin', 'python3')

    print('starting pip install')
    # get and install pip
    get_pip_file = 'get-pip.py'
    osnap.util.get('https://bootstrap.pypa.io/get-pip.py', cache_folder, get_pip_file, verbose)
    shutil.copyfile(os.path.join(cache_folder, get_pip_file), os.path.join(osnap.const.python_folder, get_pip_file))
    cmd = python_path + ' ' + os.path.join(osnap.const.python_folder, get_pip_file)
    if verbose:
        print('executing %s' % str(cmd))
    # make sure we don't detect the venv's pip and decide we already have pip
    subprocess.run(cmd, shell=True, env={})
    print('ending pip install')

    return True


def add_packages_mac(requirements, verbose):
    # install the site packages
    if requirements is None:
        print('Error: no requirements given')
        return
    pip_path = os.path.join(osnap.const.python_folder, 'bin', 'pip3')
    for requirement in requirements:
        cmd = [pip_path, 'install', '--upgrade', requirement]
        if verbose:
            print('executing %s' % str(cmd))
        subprocess.check_call(cmd)