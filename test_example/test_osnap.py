
# runs test_example as an actual test (e.g. via py.test)

import test_example.create_python_environment
import test_example.create_installer


def test_osnap(verbose=False):
    test_example.create_python_environment.create_python_environment(verbose)
    test_example.create_installer.create_installer(verbose)


if __name__ == '__main__':
    test_osnap(True)

