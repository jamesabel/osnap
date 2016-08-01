
import base64
import bz2
import time
import os
import shutil

import util


def binary_to_python(binary_path, name, python_file_path):
    """
    Takes a binary file and converts it into a python source file so that it can be found via
    a python import statement, instead of having to somehow find the binary file itself in the file system.
    """
    with open(binary_path, 'rb') as in_file:
        with open(python_file_path, 'w') as out_file:
            encoded_binary = base64.b16encode(bz2.compress(in_file.read())).decode("utf-8")
            out_file.write('# from: %s (mtime : %s, bytes : %i)\n' % (binary_path,
                                                                      time.ctime(os.path.getmtime(binary_path)),
                                                                      os.path.getsize(binary_path)))
            out_file.write(name)
            out_file.write("=\\\n")
            len_per_line = 70
            # break the encoded binary file into multiple lines so it can be brought into an editor
            # (it's really just binary data, but it's nice to be able to look at it)
            for lc in [encoded_binary[i:i+len_per_line] for i in range(0, len(encoded_binary), len_per_line)]:
                out_file.write("    '")
                out_file.write(lc)
                out_file.write("'\\\n")


def dist2py():
    dist_dir = util.get_launch_name()
    compression_type = 'zip'
    py_file_name = 'launch' + util.get_os_name() + '.py'

    print('zipping %s (%s)' % (dist_dir, os.path.abspath(dist_dir)))
    zip_file = shutil.make_archive(dist_dir, compression_type, dist_dir)
    # put the .py into the osnap directory so it is importable by the user
    py_file_path = os.path.join('..', 'osnap', py_file_name)
    print('starting to convert %s to %s' % (zip_file, py_file_path))
    binary_to_python(zip_file, dist_dir, py_file_path)
    print('done converting %s' % py_file_path)


if __name__ == '__main__':
    dist2py()
