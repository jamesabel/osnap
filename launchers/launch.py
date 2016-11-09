    
# launch.pyw - a .pyw since we're launching without a console window
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

def launch():
    VERSION = '0.0.4'
    LOGGER = logging.getLogger('osnap_launcher')

    # conventions
    python_folder = 'osnapy'

    if platform.system().lower()[0] == 'w':
        # windows
        python_binary = 'python.exe'
        python_path = os.path.join(python_folder, python_binary)

    elif platform.system().lower()[0] == 'd':
        # macOS/OSX reports 'Darwin'
        python_binary = 'python3'
        python_path = os.path.join(python_folder, 'bin', python_binary)
    else:
        raise NotImplementedError

    LOGGER.info('launcher version : %s', VERSION)
    LOGGER.info('sys.path : %s', sys.path)
    LOGGER.info('original cwd : %s', os.getcwd())

    # go up directory levels until we find our python interpreter
    # this is necessary the way various operating systems (e.g. Mac) launch in a subdirectory (e.g. Contents/MacOS)
    shortest_path_string = 5  # tolerate all OS, e.g. c:\, /, etc.
    loop_count = 0
    while not os.path.exists(python_folder) and len(os.getcwd()) > shortest_path_string and loop_count < 10:
        LOGGER.info('looking for %s at cwd : %s', python_path, os.getcwd())

        if os.path.exists(python_folder):
            LOGGER.info('%s found at %s', python_folder, os.getcwd())
            break
        # special directories to follow back 'up'
        found_special = False
        for d in ['MacOS', 'osnapp']:
            if os.path.exists(d):
                os.chdir(d)
                LOGGER.info('%s found - did a chdir to %s', d, os.getcwd())
                found_special = True
                break
        if not found_special:
            try:
                os.chdir('..')
            except IOError:
                LOGGER.error('IOError : while looking for %s in %s', python_folder, os.getcwd())
                break
        loop_count += 1

    if not os.path.exists(python_path):
        raise Exception('{} does not exist (loop_count={}) - exiting'.format(python_path, loop_count))

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
                'level'     : 'DEBUG',
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
                'handlers'  : ['file'],
                'level'     : 'DEBUG',
                'propogate' : True,
            },
        },
        'root'              : {
            'level'         : 'DEBUG',
            'handlers'      : ['file'],
        },
    })
    
    try:
        launch()
        return 0
    except Exception as e:
        logging.getLogger().exception("Unhandled exception in launcher: %s", e)
        return 1

if __name__ == '__main__':
    sys.exit(main())

