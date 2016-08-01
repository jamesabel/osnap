
import osnap.installer

import test_example.const


def create_installer(verbose):
    osnap.installer.create_installer(test_example.const.author, test_example.const.application_name,
                                     'this is my test example', 'www.mydomain.com', ['mypackage'], verbose=verbose)

if __name__ == '__main__':
    create_installer(True)
