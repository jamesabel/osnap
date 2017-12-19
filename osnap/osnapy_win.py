
import os
import platform
import subprocess
import shutil
import glob


from osnap import __application_name__, get_logger, python_folder
import osnap.make_nsis
import osnap.util
import osnap.osnapy_base

LOGGER = get_logger(__application_name__)


class OsnapyWin(osnap.osnapy_base.OsnapyBase):

    def create_python(self):
        """
        Create a full, stand-alone python installation with the required packages
        """

        cache_folder = 'cache'

        osnap.util.make_dir(python_folder, True)
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
            osnap.util.extract(cache_folder, zip_file, python_folder)
        else:
            raise Exception('could not get embeddable Python ({} from {}) - exiting'.format(zip_file, zip_url))

        # we need to use an unzipped version of pythonXX.zip since some packages can't read into the .zip
        # (e.g. https://bugs.python.org/issue24960)
        zip_list = glob.glob(os.path.join(python_folder, 'python*.zip'))
        if len(zip_list) != 1:
            raise Exception('too many zip files in {}'.format(zip_list))
        pythonxx_zip_path = zip_list[0]
        temp_file = 'temp.zip'
        temp_path = os.path.join(python_folder, temp_file)
        os.rename(pythonxx_zip_path, temp_path)
        osnap.util.extract(python_folder, temp_file,
                           os.path.join(python_folder, os.path.basename(pythonxx_zip_path)))
        os.remove(temp_path)

        python_path = os.path.join(python_folder, 'python.exe')

        # Programmatically edit ._pth file, e.g. osnapy\python36._pth
        # see https://github.com/pypa/pip/issues/4207
        glob_path = os.path.join(python_folder, 'python*._pth')
        pth_glob = glob.glob(glob_path)
        if pth_glob is None or len(pth_glob) != 1:
            LOGGER.critical("could not find '._pth' file at %s" % glob_path)
        else:
            pth_path = pth_glob[0]
            LOGGER.info('uncommenting import site in %s' % pth_path)
            pth_contents = open(pth_path).read()
            pth_save_path = pth_path.replace('._pth', '_orig._pth')
            shutil.move(pth_path, pth_save_path)
            pth_contents = pth_contents.replace('#import site', 'import site')  # uncomment import site
            pth_contents = '..\n' + pth_contents  # add where main.py will be (one dir 'up' from python.exe)
            open(pth_path, 'w').write(pth_contents)

        # get and install pip
        get_pip_file = 'get-pip.py'
        osnap.util.get('https://bootstrap.pypa.io/get-pip.py', cache_folder, get_pip_file)

        shutil.copyfile(os.path.join(cache_folder, get_pip_file), os.path.join(python_folder, get_pip_file))
        cmd = [python_path, os.path.join(python_folder, get_pip_file)]
        LOGGER.debug('Executing %s', cmd)
        subprocess.check_call(cmd)

    def pip(self, package):
        cmd = [os.path.join(python_folder, 'Scripts', 'pip.exe'), 'install', '-U']
        if package is None:
            cmd += ['-r', 'requirements.txt']
        else:
            cmd.append(package)
        cmd_str = ' '.join(cmd)
        LOGGER.debug('executing %s', cmd_str)
        return subprocess.check_call(cmd_str, shell=True)


