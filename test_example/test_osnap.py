
# runs test_example as an actual test (e.g. via py.test)

import test_example.make_osnapy
import test_example.make_installer


def test_osnap(verbose=False):
    test_example.make_osnapy.create_python_environment(verbose)
    test_example.make_installer.create_installer(verbose)


if __name__ == '__main__':
    test_osnap(True)

