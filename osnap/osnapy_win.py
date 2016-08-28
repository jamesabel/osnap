
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


def create_python_win(version, clean_cache, verbose):
    """
    Create a full, stand-alone python installation with the required packages
    """

    cache_folder = 'cache'

    osnap.util.make_dir(osnap.const.python_folder, True, verbose)
    osnap.util.make_dir(cache_folder, clean_cache, verbose)

    # get the embeddable Python .zip
    zip_file = 'python-%s-embed-amd64.zip' % version
    zip_url = 'https://www.python.org/ftp/python/%s/%s' % (version, zip_file)
    osnap.util.get(zip_url, cache_folder, zip_file, verbose)
    osnap.util.extract(cache_folder, zip_file, osnap.const.python_folder, verbose)

    # we need to use an unzipped version of pythonXX.zip since some packages can't read into the .zip
    # (e.g. https://bugs.python.org/issue24960)
    zip_list = glob.glob(os.path.join(osnap.const.python_folder, 'python*.zip'))
    if len(zip_list) != 1:
        print('error : too many zip files in %s' % str(zip_list))
        return False
    pythonxx_zip_path = zip_list[0]
    temp_file = 'temp.zip'
    temp_path = os.path.join(osnap.const.python_folder, temp_file)
    os.rename(pythonxx_zip_path, temp_path)
    osnap.util.extract(osnap.const.python_folder, temp_file,
                       os.path.join(osnap.const.python_folder, os.path.basename(pythonxx_zip_path)), verbose)
    os.remove(temp_path)

    python_path = os.path.join(osnap.const.python_folder, 'python.exe')

    # get and install pip
    get_pip_file = 'get-pip.py'
    osnap.util.get('https://bootstrap.pypa.io/get-pip.py', cache_folder, get_pip_file, verbose)
    shutil.copyfile(os.path.join(cache_folder, get_pip_file), os.path.join(osnap.const.python_folder, get_pip_file))
    cmd = [python_path, os.path.join(osnap.const.python_folder, get_pip_file)]
    if verbose:
        print('executing %s' % str(cmd))
    subprocess.check_call(cmd)


def add_package_win(package, verbose):
    # install a site package
    pip_path = os.path.join(osnap.const.python_folder, 'Scripts', 'pip.exe')
    cmd = [pip_path, 'install', '--upgrade', package]
    if verbose:
        print('executing %s' % str(cmd))
    subprocess.check_call(cmd)




