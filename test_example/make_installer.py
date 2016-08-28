
import osnap.installer

APPLICATION_NAME = 'test_example'
AUTHOR = 'test'


def create_installer(verbose):
    osnap.installer.create_installer(AUTHOR, APPLICATION_NAME,
                                     'this is my test example', 'www.mydomain.com', ['application'], verbose=verbose)


def main():
    create_installer(True)

if __name__ == '__main__':
    main()
