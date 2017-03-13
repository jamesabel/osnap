
import platform

package_name = 'osnap'

# this is the same as the launcher uses
python_folder = 'osnapy'

if platform.system().lower()[0] == 'w':
    # on windows, we can't install pip yet on 3.6 in the embedded Python
    default_python_version = '3.5.3'
else:
    default_python_version = '3.6.0'


main_program_py = 'main.py'

windows_app_dir = 'osnapp'

dist_dir = 'dist'

CACHE_FOLDER = 'cache'
TEMP_FOLDER = 'temp'

