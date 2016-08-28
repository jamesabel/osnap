
import os
from distutils.core import setup

launcher_dir = 'launchers'

setup(
    name='osnap',
    version='0.0',
    author='James Abel',
    author_email='j@abel.co',
    url='osnap.abel.co',
    data_files=[('osnap', [os.path.join(launcher_dir, 'launchmac.zip'), os.path.join(launcher_dir, 'launchwin.zip')])],
    packages=['osnap'],
)
