import logging
import os
import py_compile
import fnmatch
import zipfile
import sys
import site

import osnap.const
import osnap.util

LOGGER = logging.getLogger(__name__)

class OsnapInstaller:
    def __init__(self, python_version, application_name, author, description, url, compile_code, verbose,
                 use_pyrun=False):
        self.python_version = python_version
        self.application_name = application_name
        self.author = author
        self.description = description
        self.url = url
        self.compile_code = compile_code
        self.verbose = verbose
        self.use_pyrun = use_pyrun

    def make_installer(self):

        # If the user has been using osnap's python, you shouldn't have to compile the code here, which keeps the
        # distribution size smaller.  However, just in case the installed program is having an issue with non-compiled
        # code (e.g. it's been installed into a read-only area), we have this option.
        if self.compile_code:
            LOGGER.debug('compiling')
            for root, dirnames, filenames in os.walk(osnap.const.python_folder):
                for filename in fnmatch.filter(filenames, '*.py'):
                    path = os.path.join(root, filename)
                    # special case: don't compile Python 2 code from PyQt
                    if 'port_v2' not in path:
                        py_compile.compile(path)

        # derived classes will finish making the installer

    def unzip_launcher(self, destination):

        # find zip
        launch_zip_name = osnap.util.get_launch_name() + '.zip'
        locations = set()
        LOGGER.debug("Looking for launch zip '%s'", launch_zip_name)
        possible_locations = site.getsitepackages() + [os.path.dirname(__file__)]
        for d in possible_locations:
            LOGGER.debug("Searching site package %s", d)
            for r, _, fs in os.walk(d):
                for f in fs:
                    if f == launch_zip_name:
                        p = os.path.join(r, f)
                        if osnap.util.is_windows():
                            p = p.lower()
                        locations.add(p)
        if len(locations) != 1:
            raise Exception('Looking for exactly one {} : found {}'.format(launch_zip_name, locations))
        launch_zip_path = locations.pop()

        LOGGER.debug('unzipping %s to %s', launch_zip_path, destination)
        zip_ref = zipfile.ZipFile(launch_zip_path, 'r')
        zip_ref.extractall(destination)
        zip_ref.close()
        os.chmod(destination, 0o755)


