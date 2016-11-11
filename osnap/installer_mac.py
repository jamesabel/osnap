import logging
import os
import subprocess
import shutil
import distutils.dir_util

import osnap.const
import osnap.util
import osnap.installer_base
import osnap.make_pkgproj


LOGGER = logging.getLogger(__name__)

class OsnapInstallerMac(osnap.installer_base.OsnapInstaller):

    def make_installer(self):
        super().make_installer()

        osnap.util.rm_mk_tree(osnap.const.dist_dir)
        self.unzip_launcher(osnap.const.dist_dir)
        dist_app_path = os.path.join(osnap.const.dist_dir, self.application_name + '.app')
        # the launcher app in the zip is a generic name of 'launch.app' - rename it to our app's name
        os.rename(os.path.join(osnap.const.dist_dir, 'launch.app'), dist_app_path)

        macos_path = os.path.join(dist_app_path, 'Contents', 'MacOS')

        for d in [self.application_name, osnap.util.get_osnapy_path_in_application_dir(self.application_name)]:
            dst = os.path.join(macos_path, os.path.basename(os.path.normpath(d)))
            LOGGER.debug('copying %s to %s', d, dst)
            distutils.dir_util.copy_tree(d, dst)
        for f in [osnap.const.main_program_py]:
            LOGGER.debug('copying %s to %s', f, macos_path)
            if os.path.exists(f):
                shutil.copy2(f, macos_path)
            else:
                LOGGER.warning('expected %s (%s) to exist but it does not', f, os.path.abspath(f))

        os.chmod(os.path.join(macos_path, 'launch'), 0o777)

        # make dmg
        dmg_command = ['hdiutil', 'create', '-volname', self.application_name, '-srcfolder', os.path.abspath('dist'), '-ov',
                       '-format', 'UDZO', self.application_name + '.dmg']
        dmg_command = ' '.join(dmg_command)
        LOGGER.debug('Executing %s', dmg_command)
        subprocess.check_call(dmg_command, shell=True)

        if not self.create_installer:
            LOGGER.debug("Not creating installer - it was not requested")
            return

        # make pkg based installer
        pkgproj_path = self.application_name + '.pkgproj'
        packages_path = os.path.join(os.sep, 'usr', 'local', 'bin', 'packagesbuild')
        if not os.path.exists(packages_path):
            raise Exception((
                'Packages tool could not be found (expected at {})'
                'See http://s.sudre.free.fr/Software/Packages/about.html (Packages by Stéphane Sudre) for '
                'information on how to obtain the Packages tool.').format(packages_path))
        pkgproj_command = [packages_path, pkgproj_path]
        osnap.make_pkgproj.make_prkproj(self.application_name, pkgproj_path)
        pkgproj_command = ' '.join(pkgproj_command)
        LOGGER.debug('Executing %s', pkgproj_command)
        subprocess.check_call(pkgproj_command, shell=True)

        # todo: delete the osnapy in /Applications (actually the entire /Applications/<application_name>.app )
