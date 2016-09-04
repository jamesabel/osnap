
# the test/example application

# must be called "main.py" so that it get bundled and launched correctly

import sys
import logging
import appdirs
import os

import test_example.mymodule

APPLICATION_NAME = 'test_example'
AUTHOR = 'test_author'


def main():

    # set up logger like any normal GUI application
    logger = logging.getLogger(APPLICATION_NAME)

    log_folder = appdirs.user_log_dir(APPLICATION_NAME, AUTHOR)
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)
    log_file_path = os.path.join(log_folder, 'launch.log')
    print(log_file_path)

    file_handler = logging.FileHandler(log_file_path)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.setLevel(logging.INFO)

    # illustrate what Python we are running
    logger.info('sys.version : %s' % str(sys.version))
    logger.info('sys.path : %s' % str(sys.path))

    # run my application
    test_example.mymodule.run()

if __name__ == '__main__':
    main()
