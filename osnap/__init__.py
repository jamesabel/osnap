
# PEP 440 compliant semver (https://semver.org/)
__version__ = '0.1.0'

__application_name__ = 'osnap'
package_name = __application_name__

__author__ = 'James Abel'

# this is the same as the launcher uses
python_folder = 'osnapy'

main_program_py = 'main.py'

windows_app_dir = 'osnapp'

dist_dir = 'dist'

CACHE_FOLDER = 'cache'
TEMP_FOLDER = 'temp'

import platform

if platform.system().lower()[0] == 'w':
    default_python_version = '3.6.3'
else:
    default_python_version = '3.6.3'

from .logger import get_logger, init_logger_from_args
