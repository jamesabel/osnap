
import platform

# PEP 440 compliant
__version__ = '0.0.dev0'

# required for OSNAP
__author__ = 'test_author'
__application_name__ = 'test_example'

if platform.system().lower()[0] == 'w':
    # on windows, we can't install pip yet on 3.6 in the embedded Python
    __python_version__ = '3.5.3'
else:
    __python_version__ = '3.6.0'
