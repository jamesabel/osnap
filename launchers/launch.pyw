
# launch.pyw - a .pyw since we're launching without a console window

import os
import sys
import subprocess
import logging
import platform
import glob
import appdirs

def launch():

    VERSION = '0.0.3'

    # conventions
    python_folder = 'osnapy'
    program = 'main.py'
    author = 'abel'  # just for the launcher (not the user's app)
    application_name = 'osnap_launcher'  # just for the launcher (not the user's app)

    log_folder = appdirs.user_log_dir(application_name, author)
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)
    log_file_path = os.path.join(log_folder, 'launch.log')
    print(log_file_path)

    logger = logging.getLogger(application_name)
    file_handler = logging.FileHandler(log_file_path)
    formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.setLevel(logging.INFO)

    if platform.system().lower()[0] == 'w':
        # windows
        python_binary = 'pythonw.exe'  # use pythonw so we don't get a console window to pop up
        python_path = os.path.join(python_folder, python_binary)

    elif platform.system().lower()[0] == 'd':
        # macOS/OSX reports 'Darwin'
        python_binary = 'python3'
        python_path = os.path.join(python_folder, 'bin', python_binary)
    else:
        raise NotImplementedError

    logger.info('launcher version : %s' % VERSION)
    logger.info('sys.path : %s' % sys.path)
    logger.info('original cwd : %s' % os.getcwd())

    # go up directory levels until we find our python interpreter
    # this is necessary the way various operating systems (e.g. Mac) launch in a subdirectory (e.g. Contents/MacOS)
    shortest_path_string = 5  # tolerate all OS, e.g. c:\, /, etc.
    loop_count = 0
    while not os.path.exists(python_folder) and len(os.getcwd()) > shortest_path_string and loop_count < 10:
        logger.info('looking for %s at cwd : %s' % (python_path, os.getcwd()))

        if os.path.exists(python_folder):
            logger.info('%s found at %s' % (python_folder, os.getcwd()))
            break
        # special directories to follow back 'up'
        found_special = False
        for d in ['MacOS', 'osnapp']:
            if os.path.exists(d):
                os.chdir(d)
                logger.info('%s found - did a chdir to %s' % (d, os.getcwd()))
                found_special = True
                break
        if not found_special:
            try:
                os.chdir('..')
            except IOError:
                logger.error('IOError : while looking for %s in %s' % (python_folder, os.getcwd()))
                break
        loop_count += 1

    if not os.path.exists(python_path):
        error_string = '%s does not exist (loop_count=%d) - exiting' % (python_path, loop_count)
        logger.error(error_string)
        print(error_string)
        print('see %s' % log_file_path)
        sys.exit(error_string)

    # set up environment variables (if needed)
    if platform.system().lower()[0] == 'w':
        env_vars = None
    elif platform.system().lower()[0] == 'd':
        site_packages_pattern = python_folder + os.sep + 'lib' + os.sep + 'python*' + os.sep + 'site-packages' + os.sep
        site_packages_glob = glob.glob(site_packages_pattern)
        if len(site_packages_glob) == 0:
            error_string = '"%s" could not be found - exiting' % site_packages_pattern
            logger.error(error_string)
            sys.exit(error_string)
        elif len(site_packages_glob) > 1:
            print('warning : "%s" yielded mulitple results' % str(site_packages_glob))
        env_vars = {'PYTHONPATH': site_packages_glob[0]}
    else:
        raise NotImplementedError

    call_parameters = ' '.join([python_path, program])
    logger.info('calling : %s with env=%s' % (str(call_parameters), str(env_vars)))
    return_code = subprocess.call(call_parameters, env=env_vars, shell=True)
    logger.info('return code : %s' % str(return_code))


if __name__ == '__main__':
    launch()

