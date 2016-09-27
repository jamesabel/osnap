
from setuptools import setup

import osnap

application_name = 'osnap'
launcher_dir = 'launchers'

setup(
    name=application_name,
    description='Turns Python applications into native applications for Windows and OSX/MacOS',
    version=osnap.__version__,
    author='James Abel',
    author_email='j@abel.co',
    url='http://osnap.abel.co',
    download_url='https://github.com/jamesabel/osnap/tarball/' + osnap.__version__,
    keywords=['freeze', 'application', 'native'],

    package_data={'': ['*.pkgproj', 'launch*.zip']},

    packages=[application_name],
    install_requires=[
        'requests', 'jinja2'
    ],
    classifiers=[]
)
