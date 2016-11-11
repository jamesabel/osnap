
import osnap.osnapy

import test_example


def create_osnapy(verbose):

    osnap.osnapy.make_osnapy(test_example.__python_version__, application_name=test_example.__application_name__,
                             force_app_uninstall=True)


if __name__ == '__main__':
    create_osnapy(True)
