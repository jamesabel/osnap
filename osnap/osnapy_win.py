
import os
import subprocess
import shutil
import glob


import osnap.make_nsis
import osnap.const
import osnap.util
import osnap.osnapy_base


class OsnapyWin(osnap.osnapy_base.OsnapyBase):

    def create_python(self):
        """
        Create a full, stand-alone python installation with the required packages
        """

        cache_folder = 'cache'

        osnap.util.make_dir(osnap.const.python_folder, True, self.verbose)
        osnap.util.make_dir(cache_folder, self.clean_cache, self.verbose)

        # get the embeddable Python .zip
        zip_file = 'python-%s-embed-amd64.zip' % self.python_version
        zip_url = 'https://www.python.org/ftp/python/%s/%s' % (self.python_version, zip_file)
        if osnap.util.get(zip_url, cache_folder, zip_file, self.python_version):
            osnap.util.extract(cache_folder, zip_file, osnap.const.python_folder, self.verbose)
        else:
            print('could not get embeddable Python (%s from %s) - exiting' % (zip_file, zip_url))
            exit()

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
                           os.path.join(osnap.const.python_folder, os.path.basename(pythonxx_zip_path)), self.verbose)
        os.remove(temp_path)

        python_path = os.path.join(osnap.const.python_folder, 'python.exe')

        # get and install pip
        get_pip_file = 'get-pip.py'
        osnap.util.get('https://bootstrap.pypa.io/get-pip.py', cache_folder, get_pip_file, self.verbose)
        shutil.copyfile(os.path.join(cache_folder, get_pip_file), os.path.join(osnap.const.python_folder, get_pip_file))
        cmd = [python_path, os.path.join(osnap.const.python_folder, get_pip_file)]
        if self.verbose:
            print('executing %s' % str(cmd))
        subprocess.check_call(cmd)

    def pip(self, package):
        cmd = [os.path.join(osnap.const.python_folder, 'Scripts', 'pip.exe'), 'install', '-U']
        if package is None:
            cmd += ['-r', 'requirements.txt']
        else:
            cmd.append(package)
        cmd_str = ' '.join(cmd)
        if self.verbose:
            print('executing %s' % str(cmd_str))
        return subprocess.check_call(cmd_str, shell=True)





