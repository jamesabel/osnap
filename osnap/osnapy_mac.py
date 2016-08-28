import os
import subprocess

import osnap.const
import osnap.util


# CPATH may be needed if we have to compile cryptography
_ENV = {'CPATH': '/usr/local/opt/openssl/include'}
_CACHE_FOLDER = 'cache'
_TEMP_FOLDER = 'temp'


def create_python_mac(version, clean_cache=False, verbose=False):
    _create_base_python_mac(version, clean_cache, verbose)
    _install_pycparser(verbose)


def add_package_mac(package, verbose):
    cmd = os.path.join(osnap.const.python_folder, 'bin', 'pip3') + ' install ' + package
    if verbose:
        print('executing %s' % str(cmd))
    subprocess.check_call(cmd, shell=True, env={})


def _install_pycparser(verbose):
    '''
    pycparser from pip doesn't work with pyrun, so we have to install from source
    '''
    msg = 'installing pycparser using special workaround code'
    if verbose:
        print('start : %s' % msg)
    pycparser = 'pycparser'
    pycparser_zip_file = pycparser + '.zip'
    pycparser_dir = os.path.abspath(os.path.join(_TEMP_FOLDER, pycparser, pycparser + '-master'))
    osnap.util.get('https://github.com/eliben/pycparser/archive/master.zip', _CACHE_FOLDER, pycparser_zip_file, verbose)
    osnap.util.extract(_CACHE_FOLDER, pycparser_zip_file, os.path.join(_TEMP_FOLDER, pycparser), verbose)
    cmd = os.path.abspath(os.path.join(osnap.const.python_folder, 'bin', 'python3')) + ' setup.py install'
    if verbose:
        print(cmd)
        print(pycparser_dir)
    subprocess.run(cmd, shell=True, env=_ENV, cwd=pycparser_dir)
    if verbose:
        print('done : %s' % msg)

def _create_base_python_mac(version, clean_cache, verbose):
    """
    Create a full, stand-alone python installation with the required packages
    """

    osnap.util.make_dir(osnap.const.python_folder, True, verbose)
    osnap.util.make_dir(_CACHE_FOLDER, clean_cache, verbose)

    install_pyrun_script = 'install-pyrun.sh'
    osnap.util.get('https://downloads.egenix.com/python/install-pyrun', '.', install_pyrun_script, verbose)
    os.chmod(install_pyrun_script, 0o755)

    cmd = [install_pyrun_script]
    # version here is x.y (e.g. 3.5), not z.y.z (e.g. not 3.5.2)
    cmd.append('--python=%s' % version)
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

    if verbose:
        print('cmd : %s' % str(cmd))
        print('env : %s' % str(_ENV))
    subprocess.run(cmd, shell=True, env=_ENV)






