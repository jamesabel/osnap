
import os
from distutils.core import setup

import osnap

application_name = 'osnap'
launcher_dir = 'launchers'

setup(
    name=application_name,
    description='Turns Python applications into native applications',
    version=osnap.__version__,
    author='James Abel',
    author_email='j@abel.co',
    url='http://osnap.abel.co',
    download_url='https://github.com/jamesabel/osnap/tarball/' + osnap.__version__,
    keywords=['freeze', 'application', 'native'],
    data_files=[('osnap', [os.path.join(application_name, 'template.pkgproj'),
                           os.path.join(launcher_dir, 'launchmac.zip'),
                           os.path.join(launcher_dir, 'launchwin.zip')])],
    packages=[application_name],
    classifiers=[]
)
