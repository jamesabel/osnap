
import logging

import requests

import osnap


def check_version(app_name):
    LOGGER = logging.getLogger(app_name)

    up_to_date = None
    LOGGER.info('your osnap version : %s' % osnap.__version__)
    r = requests.get('http://api.abel.co/osnap/version')
    if r and r.status_code == 200:
        pypi_version = r.text
        LOGGER.info('PyPI osnap version : %s' % pypi_version)
        if tuple(pypi_version.split('.')) > tuple(osnap.__version__.split('.')):
            print('note: the latest osnap version is %s, your version is %s' % (pypi_version, osnap.__version__))
            up_to_date = False
        else:
            up_to_date = True
    return up_to_date
