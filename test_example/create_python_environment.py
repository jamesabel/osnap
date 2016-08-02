
import osnap.python_environment
import osnap.util
import osnap.write_timestamp


def create_python_environment(verbose):

    # we currently have slightly different versions across the OSs
    if osnap.util.is_windows():
        python_version = '3.5.2'
    elif osnap.util.is_mac():
        python_version = '3.5'
    else:
        raise NotImplementedError

    osnap.python_environment.create_python(python_version, verbose=verbose)
    osnap.python_environment.add_packages(['appdirs', 'cryptography', 'PyQt5'], verbose=verbose)
    osnap.python_environment.unpack_launcher(verbose=verbose)

if __name__ == '__main__':
    create_python_environment(True)
