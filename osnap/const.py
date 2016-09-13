
import os

package_name = 'osnap'

# this is the same as the launcher uses
python_folder = 'osnapy'

python_path = os.path.join(python_folder, 'bin', 'python3')

default_python_version = '3.5.2'

program = 'main.py'

windows_app_dir = 'osnapp'

dist_dir = 'dist'

CACHE_FOLDER = 'cache'
TEMP_FOLDER = 'temp'

# CPATH may be needed if we have to compile a package, e.g. cryptography
#
# I don't like putting PATH here like this, but I had to for SQLAlchemy else I got:
#   File "<pyrun>/os.py", line 683, in __getitem__
# KeyError: 'PATH'
ENV = {'CPATH': '/usr/local/opt/openssl/include',
       'PATH': '/opt/local/bin:/opt/local/sbin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:.'}
