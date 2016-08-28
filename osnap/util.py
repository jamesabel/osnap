
import platform
import os
import shutil
import zipfile
import tarfile
import time

import requests


def is_windows():
    return platform.system().lower()[0] == 'w'


def is_mac():
    # macOS/OSX reports 'Darwin'
    return platform.system().lower()[0] == 'd'


def get_os_name():
    if is_mac():
        return 'mac'
    elif is_windows():
        return 'win'
    else:
        raise NotImplementedError


def get_launch_name():
    return 'launch' + get_os_name()


def make_dir(path, remove, verbose):
    if remove and os.path.exists(path):
        if verbose:
            print('removing : %s' % path)
        shutil.rmtree(path)
    if not os.path.exists(path):
        if verbose:
            print('making folder : %s' % path)
            os.mkdir(path)


def extract(source_folder, source_file, destination_folder, verbose):
    source = os.path.join(source_folder, source_file)
    if verbose:
        print('extracting %s to %s' % (source, destination_folder))
    extension = source_file[-4:]
    if extension == '.zip':
        with zipfile.ZipFile(source) as zf:
            # assumes a trusted .zip
            zf.extractall(destination_folder)
    elif extension == '.tgz':
        with tarfile.open(source) as tf:
            tf.extractall(destination_folder)
    else:
        print('error : unsupported file type %s' % source_file)
        exit()


def get(url, destination_folder, file_name, verbose):
    destination_path = os.path.join(destination_folder, file_name)
    if os.path.exists(destination_path):
        if verbose:
            print('using existing copy of %s from %s' % (file_name, os.path.abspath(destination_path)))
    else:
        if verbose:
            print('get %s to %s' % (url, destination_path))
        response = requests.get(url, stream=True)
        with open(destination_path, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response


def rm_mk_tree(dir_path):
    '''
    Clears out a dir.  Makes it if it doesn't exist.
    :param dir_path: dir to clear out
    :return: True on success
    '''

    # fancy rmtree, since for some reason shutil.rmtree can return before the tree is actually removed
    count = 600
    while os.path.exists(dir_path) and count > 0:
        try:
            shutil.rmtree(dir_path)
        except FileNotFoundError:
            pass
        except IOError:
            time.sleep(0.1)
        count -= 1

    os.mkdir(dir_path)

    return count > 0
