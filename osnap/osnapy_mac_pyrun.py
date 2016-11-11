import logging
import subprocess
import os

import osnap.const
import osnap.util
import osnap.osnapy_base

LOGGER = logging.getLogger(__name__)

class OsnapyMacPyrun(osnap.osnapy_base.OsnapyBase):

    def add_package(self, package):
        super().add_package(package)
        cmd = os.path.join(osnap.const.python_folder, 'bin', 'pip3') + ' install ' + package
        LOGGER.debug('executing %s', cmd)
        subprocess.check_call(cmd, shell=True, env={})

    def create_python(self):

        print('notice: the pyrun version is likely to be deprecated in favor of the osnap build')

        osnap.util.make_dir(osnap.const.python_folder, True)
        osnap.util.make_dir(osnap.const.CACHE_FOLDER, self.clean_cache)

        install_pyrun_script = 'install-pyrun.sh'
        osnap.util.get('https://downloads.egenix.com/python/install-pyrun', '.', install_pyrun_script)
        os.chmod(install_pyrun_script, 0o755)

        cmd = [install_pyrun_script]
        # version here is x.y (e.g. 3.5), not z.y.z (e.g. not 3.5.2)
        cmd.append('--python=%s' % self.python_version)
        # version 2.2.1 produces a "Segmentation fault: 11" error when python is run so use a prior version.
        cmd.append('--pyrun=2.2.0')

        # pip version explicit specification is a workaround since "--pip-version=latest" doesn't work
        # for install-pyrun.sh ( I get "sed: illegal option -- r" ).  Also, same for setuptools.
        # todo: either get the script fixed or dynamically determine the latest pip and setuptools
        cmd.append('--pip-version=8.1.2')
        cmd.append('--setuptools-version=26.0.0')

        cmd.append('-l')  # log

        cmd.append(osnap.const.python_folder)

        cmd = ' '.join(cmd)  # shell=True needs a string, not a list

        LOGGER.debug('cmd : %s', cmd)
        LOGGER.debug('env : %s', osnap.const.ENV)
        subprocess.run(cmd, shell=True, env=osnap.const.ENV)
