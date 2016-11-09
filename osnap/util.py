import logging
import platform
import os
import shutil
import zipfile
import tarfile
import time

import requests

import osnap.const

LOGGER = logging.getLogger(__name__)

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


def get_launch_name(architecture, variant):
    if is_mac():
        return 'launchmac'
    elif is_windows():
        if variant == 'console':
            if architecture == '32bit':
                return 'launchwin-x86-console'
            elif architecture == '64bit':
                return 'launchwin-amd64-console'
        else:
            if architecture == '32bit':
                return 'launchwin-x86-window'
            elif architecture == '64bit':
                return 'launchwin-amd64-window'
        raise Exception("Unrecognized architecture {} for windows".format(architecture))
    else:
        raise Exception("Unrecognized operating system")

def make_dir(path, remove):
    if remove and os.path.exists(path):
        LOGGER.debug('removing : %s', path)
        shutil.rmtree(path)
    if not os.path.exists(path):
        LOGGER.debug('making folder : %s', path)
        os.mkdir(path)


def extract(source_folder, source_file, destination_folder):
    source = os.path.join(source_folder, source_file)
    LOGGER.debug('extracting %s to %s', source, destination_folder)
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
        raise Exception('Unsupported file type {} (extension : {})'.format(source_file, extension))


def tgz(source_dir, tgz_file_path):
    LOGGER.debug('tgz-ing %s (%s) to %s (%s)', source_dir, os.path.abspath(source_dir), tgz_file_path, os.path.abspath(tgz_file_path))
    with tarfile.open(tgz_file_path, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))


def get(url, destination_folder, file_name):
    destination_path = os.path.join(destination_folder, file_name)
    if os.path.exists(destination_path):
        LOGGER.info('using existing copy of %s from %s', file_name, os.path.abspath(destination_path))
    else:
        LOGGER.info('get %s to %s', url, destination_path)
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(destination_path, 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            del response
        else:
            raise Exception('error getting {} from {}'.format(file_name, url))
    return True


def rm_mk_tree(dir_path):
    '''
    Clears out a dir.  Makes it if it doesn't exist.
    :param dir_path: dir to clear out
    :return: True on success
    '''

    # fancy rmtree, since for some reason shutil.rmtree can return before the tree is actually removed
    count = 0
    LOGGER.debug('removing %s (%s)', dir_path, os.path.abspath(dir_path))
    while os.path.exists(dir_path) and count < 30:
        try:
            shutil.rmtree(dir_path)
        except FileNotFoundError:
            pass
        except IOError:
            if count > 1:
                LOGGER.info('retrying removal of %s - perhaps you need to run this as sudo?', dir_path)
            time.sleep(2)
        count += 1
    if os.path.exists(dir_path):
        raise Exception('error: could not remove {} - exiting'.format(dir_path))

    LOGGER.info('making %s (%s)', dir_path, os.path.abspath(dir_path))
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
