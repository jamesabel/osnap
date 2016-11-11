import logging
import os
import platform
import subprocess
import shutil
import glob


import osnap.make_nsis
import osnap.const
import osnap.util
import osnap.osnapy_base

LOGGER = logging.getLogger(__name__)

class OsnapyWin(osnap.osnapy_base.OsnapyBase):

    def create_python(self):
        """
        Create a full, stand-alone python installation with the required packages
        """

        cache_folder = 'cache'

        osnap.util.make_dir(osnap.const.python_folder, True)
        osnap.util.make_dir(cache_folder, self.clean_cache)

        # get the embeddable Python .zip
        if self.architecture == '64bit':
            zip_file = 'python-%s-embed-amd64.zip' % self.python_version
        elif self.architecture == '32bit':
            zip_file = 'python-%s-embed-win32.zip' % self.python_version
        else:
            raise Exception("Sorry, we don't currently support your architecture on windows ({}). Please submit a ticket at https://github.com/jamesabel/osnap/issues/".format(platform.machine()))

        zip_url = 'https://www.python.org/ftp/python/{}/{}'.format(self.python_version, zip_file)
        LOGGER.debug("Getting embeddable python from %s", zip_url)
        if osnap.util.get(zip_url, cache_folder, zip_file):
            osnap.util.extract(cache_folder, zip_file, osnap.const.python_folder)
        else:
            raise Exception('could not get embeddable Python ({} from {}) - exiting'.format(zip_file, zip_url))

        # we need to use an unzipped version of pythonXX.zip since some packages can't read into the .zip
        # (e.g. https://bugs.python.org/issue24960)
        zip_list = glob.glob(os.path.join(osnap.const.python_folder, 'python*.zip'))
        if len(zip_list) != 1:
            raise Exception('too many zip files in {}'.format(zip_list))
        pythonxx_zip_path = zip_list[0]
        temp_file = 'temp.zip'
        temp_path = os.path.join(osnap.const.python_folder, temp_file)
        os.rename(pythonxx_zip_path, temp_path)
        osnap.util.extract(osnap.const.python_folder, temp_file,
                           os.path.join(osnap.const.python_folder, os.path.basename(pythonxx_zip_path)))
        os.remove(temp_path)

        python_path = os.path.join(osnap.const.python_folder, 'python.exe')

        # get and install pip
        get_pip_file = 'get-pip.py'
        osnap.util.get('https://bootstrap.pypa.io/get-pip.py', cache_folder, get_pip_file)

        shutil.copyfile(os.path.join(cache_folder, get_pip_file), os.path.join(osnap.const.python_folder, get_pip_file))
        cmd = [python_path, os.path.join(osnap.const.python_folder, get_pip_file)]
        LOGGER.debug('Executing %s', cmd)
        subprocess.check_call(cmd)

    def pip(self, package):
        cmd = [os.path.join(osnap.const.python_folder, 'Scripts', 'pip.exe'), 'install', '-U']
        if package is None:
            cmd += ['-r', 'requirements.txt']
        else:
            cmd.append(package)
        cmd_str = ' '.join(cmd)
        LOGGER.debug('executing %s', cmd_str)
        return subprocess.check_call(cmd_str, shell=True)





