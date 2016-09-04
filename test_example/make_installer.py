
import osnap.installer

APPLICATION_NAME = 'test_example'
AUTHOR = 'test'


def make_installer(verbose):
    osnap.installer.make_installer(AUTHOR, APPLICATION_NAME, 'this is my test example', 'www.mydomain.com',
                                   [APPLICATION_NAME], verbose=verbose)


if __name__ == '__main__':
    make_installer(True)
