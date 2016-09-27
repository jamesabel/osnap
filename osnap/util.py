
import platform
import os
import shutil
import zipfile
import tarfile
import time

import requests

import osnap.const


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
    extension = source_file[source_file.rfind('.')+1:]
    if extension == 'zip':
        with zipfile.ZipFile(source) as zf:
            # assumes a trusted .zip
            zf.extractall(destination_folder)
    elif extension == 'tgz':
        with tarfile.open(source) as tf:
            tf.extractall(destination_folder)
    elif extension == 'gz':
        with tarfile.open(source) as tf:
            tf.extractall(destination_folder)
    else:
        print('error : unsupported file type %s (extension : %s)' % (source_file, extension))
        exit()


def tgz(source_dir, tgz_file_path, verbose):
    if verbose:
        print('tgz-ing %s (%s) to %s (%s)' % (source_dir, os.path.abspath(source_dir), tgz_file_path,
                                              os.path.abspath(tgz_file_path)))
    with tarfile.open(tgz_file_path, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))


def get(url, destination_folder, file_name, verbose):
    destination_path = os.path.join(destination_folder, file_name)
    if os.path.exists(destination_path):
        if verbose:
            print('using existing copy of %s from %s' % (file_name, os.path.abspath(destination_path)))
    else:
        if verbose:
            print('get %s to %s' % (url, destination_path))
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(destination_path, 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            del response
        else:
            print('error getting %s from %s' % (file_name, url))
            return False
    return True


def rm_mk_tree(dir_path, verbose=False):
    '''
    Clears out a dir.  Makes it if it doesn't exist.
    :param dir_path: dir to clear out
    :param verbose: print debug messages
    :return: True on success
    '''

    # fancy rmtree, since for some reason shutil.rmtree can return before the tree is actually removed
    count = 0
    if verbose:
        print('removing %s (%s)' % (dir_path, os.path.abspath(dir_path)))
    while os.path.exists(dir_path) and count < 30:
        try:
            shutil.rmtree(dir_path)
        except FileNotFoundError:
            pass
        except IOError:
            if count > 1:
                print('retrying removal of %s - perhaps you need to run this as sudo?' % dir_path)
            time.sleep(2)
        count += 1
    if os.path.exists(dir_path):
        msg = 'error: could not remove %s - exiting' % dir_path
        print(msg)
        exit(msg)

    if verbose:
        print('making %s (%s)' % (dir_path, os.path.abspath(dir_path)))
    os.makedirs(dir_path)

    return count > 0


def get_osnapy_tgz_file_and_url(python_version, os_version):
    # https://s3.amazonaws.com/abel.co/osnapy/osnapy_3.5.2_osx.tgz
    tgz_file = 'osnapy_%s_%s.tgz' % (python_version, os_version)
    return tgz_file, 'https://s3.amazonaws.com/abel.co/osnapy/%s' % tgz_file


def get_application_dir(application_name):
    return os.path.join(os.sep, 'Applications', application_name + '.app')


def get_osnapy_path_in_application_dir(application_name):
    # We're building right into the /Application directory which I don't like, but Python's build process
    # on Mac requires an absolute path so we have to create osnapy explicitly in its final resting place.
    # This will require sudo for the "make install".
    # Reference: http://www.diveintopython.net/installing_python/source.html
    # Hopefully eventually the install dir won't have to be an absolute path.
    return os.path.join(get_application_dir(application_name), 'Contents', 'MacOS', osnap.const.python_folder)