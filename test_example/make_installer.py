
import osnap.installer

import test_example


def make_installer(verbose):
    osnap.installer.make_installer(test_example.__python_version__, test_example.__application_name__,
                                   test_example.__author__, 'this is my test example', 'www.mydomain.com',
                                   )


if __name__ == '__main__':
    make_installer(True)
