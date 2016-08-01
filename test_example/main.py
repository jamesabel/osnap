
# the test/example application

import sys
import logging

import mypackage.mymodule


def main():

    # set up logger like any normal GUI application
    logger = logging.getLogger('test_example')
    file_handler = logging.FileHandler('test_example.log')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.setLevel(logging.INFO)

    # illustrate what Python we are running
    logger.info('sys.version : %s' % str(sys.version))
    logger.info('sys.path : %s' % str(sys.path))

    # run my application
    mypackage.mymodule.run()

if __name__ == '__main__':
    main()
