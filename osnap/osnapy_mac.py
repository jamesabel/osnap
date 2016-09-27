import os
import subprocess
try:
    import pwd
except ImportError:
    pass

import osnap.const
import osnap.util
import osnap.osnapy_base


class OsnapyMac(osnap.osnapy_base.OsnapyBase):

    def pip(self, package):
        pip_path = os.path.join(osnap.util.get_osnapy_path_in_application_dir(self.application_name), 'bin', 'pip3')
        cmd = ['sudo', '-H', pip_path, 'install', '-U']
        if package is None:
            cmd += ['-r', 'requirements.txt']
        else:
            cmd.append(package)
        cmd_str = ' '.join(cmd)
        if self.verbose:
            print('executing %s' % str(cmd_str))
        return subprocess.check_call(cmd_str, shell=True)

    def create_python(self):

        if os.getuid() != 0:
            s = 'error: must execute as root (i.e. "sudo -H <command>") - you are "%s"' % pwd.getpwuid(os.getuid())[0]
            print(s)
            exit(s)

        if self.verbose:
            print('running as "%s"' % pwd.getpwuid(os.getuid())[0])

        root_dir = osnap.const.TEMP_FOLDER
        base_dir = os.path.join(root_dir, 'build_osx')
        cache_dir = os.path.join(root_dir, osnap.const.CACHE_FOLDER)
        logs_dir = os.path.abspath('logs')
        application_dir = osnap.util.get_application_dir(self.application_name)
        prefix_dir = osnap.util.get_osnapy_path_in_application_dir(self.application_name)
        python_str = 'Python-%s' % self.python_version
        source_file = python_str + '.tgz'

        # e.g. https://www.python.org/ftp/python/3.5.2/Python-3.5.2.tgz
        source_url = 'http://www.python.org/ftp/python/%s/%s' % (self.python_version, source_file)

        if self.verbose:
            print('cwd : %s (%s)' % (os.getcwd(), os.path.abspath(os.getcwd())))
            print('base_dir : %s (%s)' % (base_dir, os.path.abspath(base_dir)))
            print('cache_dir : %s (%s)' % (cache_dir, os.path.abspath(cache_dir)))
            print('logs_dir : %s' % logs_dir)
            print('python_str : %s' % python_str)
            print('source_file : %s' % source_file)
            print('source_url : %s' % source_url)
            print('prefix_dir : %s' % prefix_dir)
            print('logs_dir : %s' % logs_dir)

        if os.path.exists(application_dir):
            if self.force_uninstalls:
                osnap.util.rm_mk_tree(application_dir)
            else:
                s = 'error : the application "%s" already exists at %s - please uninstall before continuing' % \
                    (self.application_name, application_dir)
                print(s)
                exit(s)

        if self.clean_cache:
            osnap.util.rm_mk_tree(cache_dir)
        try:
            os.makedirs(cache_dir)
        except FileExistsError:
            pass

        osnap.util.rm_mk_tree(base_dir, self.verbose)
        osnap.util.rm_mk_tree(prefix_dir, self.verbose)
        osnap.util.rm_mk_tree(logs_dir, self.verbose)

        osnap.util.get(source_url, cache_dir, source_file, self.verbose)
        osnap.util.extract(cache_dir, source_file, base_dir, self.verbose)

        save_cwd = os.getcwd()
        os.chdir(os.path.join(base_dir, python_str))

        # todo: a check for xcode
        # todo: a check for SSL

        self._make_call(' '.join(['./configure', '--enable-shared=no', '--prefix=%s' % prefix_dir]), logs_dir,
                  'configure')
        self._make_call('make', logs_dir, 'make')
        self._make_call('make install', logs_dir, 'make_install')

        os.chdir(save_cwd)

    def _make_call(self, cmd_str, logs_dir, label):
        if self.verbose:
            print(cmd_str)
        env = {'CPPFLAGS': '-I/usr/local/opt/openssl/include',
               'LDFLAGS': '-L/usr/local/opt/openssl/lib',
               'PATH': '/opt/local/bin:/opt/local/sbin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin'}
        subprocess.check_call(cmd_str, env=env, shell=True,
                              stdout=open(os.path.join(logs_dir, label + '.log'), 'w'),
                              stderr=open(os.path.join(logs_dir, label + '_err.log'), 'w'))
