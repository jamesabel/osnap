
import os
import logging
import logging.handlers
import shutil

import appdirs

from osnap import __application_name__, __author__


g_formatter = logging.Formatter('%(asctime)s - %(name)s - %(filename)s - %(lineno)s - %(funcName)s - %(levelname)s - %(message)s')


def get_logger(name):
    """
    Special "get logger" where you can pass in __file__ and it extracts the module name, or a string that is
    the application name.
    :param name: name of the logger to get, optionally as a python file path
    :return: a logger
    """

    # If name is a python file, or a path to a python file, extract the module name.  Otherwise just use name
    # as is.
    if os.sep in name:
        name = name.split(os.sep)[-1]
    if name.endswith('.py'):
        name = name[:-3]
    return logging.getLogger(name)


log = get_logger(__application_name__)

handlers = {}


def init_logger(name, author=None, log_directory=None, verbose=False, delete_existing_log_files=False,
                max_bytes=100*1E6, backup_count=3):
    """
    Initialize the logger.  Call once from the application 'main'.
    """

    global handlers

    root_log = logging.getLogger()  # we init the root logger so all child loggers inherit this functionality

    if root_log.hasHandlers():
        root_log.error('logger already initialized')
        return root_log

    if verbose:
        root_log.setLevel(logging.DEBUG)
    else:
        root_log.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(g_formatter)
    if verbose:
        console_handler.setLevel(logging.INFO)
    else:
        console_handler.setLevel(logging.WARNING)
    root_log.addHandler(console_handler)
    handlers['console'] = console_handler

    # create file handler
    if log_directory is None:
        log_directory = appdirs.user_log_dir(name, author)
    if delete_existing_log_files:
        shutil.rmtree(log_directory, ignore_errors=True)
    os.makedirs(log_directory, exist_ok=True)
    fh_path = os.path.join(log_directory, '%s.log' % name)
    file_handler = logging.handlers.RotatingFileHandler(fh_path, maxBytes=max_bytes, backupCount=backup_count)
    file_handler.setFormatter(g_formatter)
    if verbose:
        file_handler.setLevel(logging.DEBUG)
    else:
        file_handler.setLevel(logging.INFO)
    root_log.addHandler(file_handler)
    handlers['file'] = file_handler
    root_log.info('log file path : "%s" ("%s")' % (fh_path, os.path.abspath(fh_path)))

    return root_log, handlers, fh_path


def set_verbose(verbose=True):
    if verbose:
        log.setLevel(logging.DEBUG)
        handlers['file'].setLevel(logging.DEBUG)
        handlers['console'].setLevel(logging.INFO)
        handlers['dialog'].setLevel(logging.WARNING)
    else:
        log.setLevel(logging.INFO)
        handlers['file'].setLevel(logging.INFO)
        handlers['console'].setLevel(logging.WARNING)
        handlers['dialog'].setLevel(logging.ERROR)


def init_logger_from_args(args):
    return init_logger(__application_name__, __author__, verbose=args.verbose)
