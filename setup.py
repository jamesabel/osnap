
import os
from distutils.core import setup

launcher_dir = 'launchers'

setup(
    name='osnap',
    description='Turns Python applications into native applications',
    version='0.0.0',
    author='James Abel',
    author_email='j@abel.co',
    url='http://osnap.abel.co',
    download_url='https://github.com/jamesabel/osnap/tarball/0.0.0',
    keywords=['freeze', 'application', 'native'],
    data_files=[('osnap', [os.path.join(launcher_dir, 'launchmac.zip'), os.path.join(launcher_dir, 'launchwin.zip')])],
    packages=['osnap'],
    classifiers=[]
)
