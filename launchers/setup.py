import sys

import util

APP = 'launch.pyw'

if util.is_mac():
    from setuptools import setup
    setup(
        app=[APP],
        options={'py2app': {'dist_dir': util.get_launch_name(),
                            'iconfile': 'circle.icns'}},
        setup_requires=['py2app'],
    )
elif util.is_windows():
    # Windows
    from setuptools import setup
    import py2exe
    try:
        import appdirs
    except ImportError:
        raise Exception((
            "You must have appdirs installed to build the launchers on windows."
            "Try pip installing them with 'pip install appdirs'"))
            
    if '3.5' in sys.version:
        raise Exception((
            "You cannot build the launcher on windows with Python 3.5."
            "py2exe only supports up to python 3.4. Please install python 3.4 and "
            "run this script using that installation"))
    setup(
        #windows=[APP],
        windows=[{"script": APP,
                  "icon_resources": [(1, "circle32x32.ico")]}],
        options={'py2exe' : {'dist_dir': util.get_launch_name()}},
        zipfile=None,
    )
else:
    raise NotImplementedError

