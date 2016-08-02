

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
    setup(
        #windows=[APP],
        windows=[{"script": APP,
                  "icon_resources": [(1, "circle32x32.ico")]}],
        options={'py2exe' : {'dist_dir': util.get_launch_name()}},
        zipfile=None,
    )
else:
    raise NotImplementedError

