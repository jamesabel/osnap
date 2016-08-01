
import platform


def is_windows():
    return platform.system().lower()[0] == 'w'


def is_mac():
    # macOS/OSX reports 'Darwin'
    return platform.system().lower()[0] == 'd'


def get_os_name():
    if is_mac():
        return 'mac'
    elif is_windows():
        return 'win'
    else:
        raise NotImplementedError


def get_launch_name():
    return 'launch' + get_os_name()

