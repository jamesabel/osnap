import sys

import util

WINDOW_APP = 'launch.pyw'
CONSOLE_APP = 'launch.py'

def main():
    if util.is_mac():
        from setuptools import setup
        setup(
            app=[WINDOW_APP],
            options={'py2app': {'dist_dir': util.get_launch_name(),
                                'iconfile': 'circle.icns'}},
            setup_requires=['py2app'],
        )
    elif util.is_windows():
        # Windows
        from setuptools import setup
        from setuptools.command.install import install
        import py2exe
        import py2exe.distutils_buildexe
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

        class InstallCommand(py2exe.distutils_buildexe.py2exe):
            user_options = install.user_options + [
                ('variant=', None, 'Specify the variant of the launcher to create'),
            ]
            def initialize_options(self):
                super().initialize_options()
                self.variant = 'window'

            def finalize_options(self):
                super().finalize_options()
                assert self.variant in ('console', 'window'), "You must specify either window or console as the variant"

            def run(self):
                if self.variant == 'window':
                    self.distribution.windows = self.distribution.windows
                elif self.variant == 'console':
                    self.distribution.console = self.distribution.windows
                    self.distribution.console[0]['script'] = CONSOLE_APP
                    self.distribution.windows = []
                else:
                    raise Exception("Unrecognized variant {}".format(self.variant))
                super().run()

        setup(
            cmdclass={
                'py2exe': InstallCommand,
            },
            windows=[{
                "icon_resources": [(1, "circle32x32.ico")],
                "script"        : WINDOW_APP,
            }],
            options={'py2exe' : {'dist_dir': util.get_launch_name()}},
            zipfile=None,
        )
    else:
        raise NotImplementedError

if __name__ == '__main__':
    main()
