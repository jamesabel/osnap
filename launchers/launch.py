
# This file exists under 2 names.  The 'real' one is launch.py.
# launch.pyw is a hard link to launch.py
# (launch.pyw - a .pyw since we're launching without a console window)

import appdirs
import glob
import logging
import logging.config
import os
import platform
import sys
import subprocess

# Just for the launcher, not the user's app that OSNAP is launching
AUTHOR = 'abel'
APPLICATION = 'osnap_launcher'
PROGRAM = 'main.py'


def find_osnapy(path_leaf):
    """
    go up directory levels until we find our python interpreter
    this is necessary the way various operating systems (e.g. Mac) launch in a subdirectory (e.g. Contents/MacOS)
    """
    LOGGER = logging.getLogger('osnap_launcher')
    path = path_leaf
    while path != os.path.dirname(path):
        potential_path = os.path.join(path, 'osnapy')
        LOGGER.debug("potential_path : %s" % potential_path)
        if os.path.exists(potential_path):
            LOGGER.debug("Found osnapy at %s", potential_path)
            return potential_path

        # special directories to follow back 'up'
        for d in ['MacOS', 'osnapp']:
            potential_path = os.path.join(path, d, 'osnapy')
            if os.path.exists(potential_path):
                LOGGER.debug("Found osnapy at %s", potential_path)
                return potential_path
        path = os.path.dirname(path)
    return None


def pick_osnapy(python_folder):
    "Find the osnapy directory and chdir to it"
    LOGGER = logging.getLogger('osnap_launcher')
    potential_paths = []
    if len(sys.argv) > 1:
        # first, try the folder that contains our target
        potential_paths.append(os.path.dirname(sys.argv[1]))
    # next, try the folder that contains the launcher
    potential_paths.append(os.path.dirname(sys.argv[0]))
    # finally, try the folder we are starting from
    potential_paths.append(os.getcwd())
    LOGGER.debug('looking in %s' % potential_paths)
    for potential_path in potential_paths:
        osnapy_path = find_osnapy(potential_path)
        if osnapy_path:
            if os.path.exists(osnapy_path):
                os.chdir(os.path.dirname(osnapy_path))
                return


def launch():
    VERSION = '0.0.6'
    LOGGER = logging.getLogger('osnap_launcher')

    # conventions
    python_folder = 'osnapy'

    if platform.system().lower()[0] == 'w':
        # windows
        python_binary = 'pythonw.exe'
        python_path = os.path.join(python_folder, python_binary)

    elif platform.system().lower()[0] == 'd':
        # macOS/OSX reports 'Darwin'
        python_binary = 'python3'
        python_path = os.path.join(python_folder, 'bin', python_binary)
    else:
        raise NotImplementedError

    LOGGER.info('launcher version : %s', VERSION)
    LOGGER.info('sys.path : %s', sys.path)
    LOGGER.info('sys.argv : %s', sys.argv)
    LOGGER.info('original cwd : %s', os.getcwd())

    pick_osnapy(python_folder)

    if not os.path.exists(python_path):
        raise Exception('{} does not exist - exiting'.format(python_path))

    # set up environment variables (if needed)
    if platform.system().lower()[0] == 'w':
        env_vars = None
    elif platform.system().lower()[0] == 'd':
        site_packages_pattern = python_folder + os.sep + 'lib' + os.sep + 'python*' + os.sep + 'site-packages' + os.sep
        site_packages_glob = glob.glob(site_packages_pattern)
        if len(site_packages_glob) == 0:
            raise Exception('"{}" could not be found - exiting'.format(site_packages_pattern))
        elif len(site_packages_glob) > 1:
            LOGGER.warning('warning : "%s" yielded mulitple results', site_packages_glob)
        env_vars = {'PYTHONPATH': site_packages_glob[0]}
    else:
        raise NotImplementedError("The platform '{}' is not supported by OSNAP yet".format(platform.system()))

    call_parameters = ' '.join([python_path, PROGRAM])
    LOGGER.info('calling : %s with env=%s', call_parameters, env_vars)
    return_code = subprocess.call(call_parameters, env=env_vars, shell=True)
    LOGGER.info('return code : %s', return_code)


def main():
    logfile = os.path.join(appdirs.user_log_dir(APPLICATION, AUTHOR), 'osnap_launcher.log')
    logdir = os.path.dirname(logfile)
    if not os.path.exists(logdir):
        os.makedirs(logdir)
    logging.config.dictConfig({
        'version'           : 1,
        'formatters'        : {
            'detailed'      : {
                'format'    : '[%(asctime)s] %(levelname)s pid:%(process)d %(name)s:%(lineno)d %(message)s',
                'dateformat': '%d/%b/%Y:%H:%M:%S %z',
            },
            'simple'        : {
                'format'    : '[%(asctime)s] %(levelname)s %(name)s:%(lineno)d %(message)s',
                'dateformat': '%d/%b/%Y:%H:%M:%S %z',
            },
        },
        'handlers'          : {
            'console'       : {
                'class'     : 'logging.StreamHandler',
                # 'level' needs to be WARNING or above - if it's DEBUG Windows will try to make a log file for GUI apps,
                # which is either an access error or pops up as an annoying dialog box.
                'level'     : 'ERROR',
                'formatter' : 'simple',
            },
            'file'          : {
                'class'     : 'logging.FileHandler',
                'filename'  : logfile,
                'formatter' : 'detailed',
                'level'     : 'DEBUG',
            },
        },
        'loggers'           : {
            ''              : {
                'handlers'  : ['file', 'console'],
                'level'     : 'DEBUG',
                'propogate' : True,
            },
        },
        'root'              : {
            'level'         : 'DEBUG',
            'handlers'      : ['file', 'console'],
        },
    })
    logging.getLogger().info("Installed logging")
    try:
        launch()
        return 0
    except Exception as e:
        logging.getLogger().exception("Unhandled exception in launcher: %s", e)
        return 1

if __name__ == '__main__':
    sys.exit(main())

