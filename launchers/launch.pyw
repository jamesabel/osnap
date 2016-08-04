
# launch.pyw - a .pyw since we're launching without a console window

import os
import subprocess
import appdirs
import logging
import platform

# conventions
python_folder = 'osnapy'
program = 'main.py'
author = 'abel'  # just for the launcher (not the user's app)
application_name = 'osnap'  # just for the launcher (not the user's app)
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


def launch():

    log_folder = appdirs.user_log_dir(application_name, author)
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)
    log_file_path = os.path.join(log_folder, 'launch.log')
    print(log_file_path)

    logger = logging.getLogger(application_name)
    file_handler = logging.FileHandler(log_file_path)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.setLevel(logging.INFO)

    logger.info('original cwd : %s' % os.getcwd())

    # go up directory levels until we find our python interpreter
    # this is necessary the way various operating systems (e.g. Mac) launch in a subdirectory (e.g. Contents/MacOS)
    shortest_path_string = 5  # tolerate all OS, e.g. c:\, /, etc.
    while len(os.getcwd()) > shortest_path_string:
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

    if os.path.exists(python_path):
        call_parameters = [python_path, program]
        logger.info('calling : %s' % str(call_parameters))
        return_code = subprocess.call(call_parameters)
        logger.info('return code : %s' % str(return_code))
    else:
        error_string = '%s does not exist' % python_path
        logger.error(error_string)
        print(error_string)
        print('see %s' % log_file_path)


if __name__ == '__main__':
    launch()

