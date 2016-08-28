
import base64
import bz2
import time
import os
import shutil

import util


def main():
    dist_dir = util.get_launch_name()
    print('zipping %s (%s)' % (dist_dir, os.path.abspath(dist_dir)))
    shutil.make_archive(dist_dir, 'zip', dist_dir)

if __name__ == '__main__':
    main()
