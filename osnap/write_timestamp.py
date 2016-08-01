
import datetime
import os
import time


def write_timestamp(base_folder="."):
    ts = datetime.datetime.now()
    file_path = os.path.join(base_folder, '_build_.py')
    with open(file_path, 'w') as f:
        f.write('timestamp = "%s"\n' % ts)
        version = int((ts.year % 100) * 10000 + ts.month * 100 + ts.day)  # year month day
        f.write('version = %d\n' % version)
        f.write('seconds_since_epoch = %d\n' % time.time())
        f.write('file_path = r"%s"\n' % file_path)
        f.write('abs_file_path = r"%s"\n' % os.path.abspath(file_path))
    return ts

if __name__ == '__main__':
    write_timestamp()