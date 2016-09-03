
import os

# this is the same as the launcher uses
python_folder = 'osnapy'

python_path = os.path.join(python_folder, 'bin', 'python3')

default_python_version = '3.5.2'

program = 'main.py'

windows_app_dir = 'osnapp'

CACHE_FOLDER = 'cache'
TEMP_FOLDER = 'temp'

# CPATH may be needed if we have to compile cryptography
ENV = {'CPATH': '/usr/local/opt/openssl/include'}