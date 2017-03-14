import logging
import os
import subprocess
import shutil
import distutils.dir_util

import lxml.etree as ElementTree

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
            if os.path.exists(d):
                dst = os.path.join(macos_path, os.path.basename(os.path.normpath(d)))
                LOGGER.info('copying %s to %s' % (d, dst))
                distutils.dir_util.copy_tree(d, dst)
            else:
                LOGGER.warning('%s does not exist' % d)

        for f in [osnap.const.main_program_py]:
            LOGGER.info('copying %s to %s' % (f, macos_path))
            if os.path.exists(f):
                shutil.copy2(f, macos_path)
            else:
                LOGGER.warning('expected %s (%s) to exist but it does not' % (f, os.path.abspath(f)))

        # mac icon file
        icon_file_name = 'icon.icns'
        src = os.path.join('icons', icon_file_name)
        if os.path.exists(src):
            dst = os.path.join(dist_app_path, 'Contents', 'Resources', icon_file_name)
            if os.path.exists(dst):
                # there should be a default file already there
                os.remove(dst)
            else:
                # if the default icon file does not exist, something is very wrong
                LOGGER.error('default icon file %s does not already exist' % dst)
            LOGGER.info('copying %s to %s' % (src, dst))
            shutil.copy2(src, dst)
        else:
            LOGGER.warning(
                '%s (%s) does not exist - using default icons.\n'
                'This will work for one program but MacOS will not install more than one program with the same icon\n'
                'so it should be fixed for any program you plan on distributing.' % (src, os.path.abspath(src)))

        # fix up the keys in the Info.plist file
        reverse_dns_identifier = self._info_plist_substitute(os.path.join(dist_app_path, 'Contents', 'Info.plist'))

        os.chmod(os.path.join(macos_path, 'launch'), 0o777)

        # make dmg
        dmg_command = ['hdiutil', 'create', '-volname', self.application_name, '-srcfolder', os.path.abspath('dist'), '-ov',
                       '-format', 'UDZO', self.application_name + '.dmg']
        dmg_command = ' '.join(dmg_command)
        LOGGER.debug('Executing %s' % dmg_command)
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
        osnap.make_pkgproj.make_pkgproj(self.application_name, reverse_dns_identifier, pkgproj_path)
        pkgproj_command = ' '.join(pkgproj_command)
        LOGGER.debug('Executing %s' % pkgproj_command)
        subprocess.check_call(pkgproj_command, shell=True)

        # todo: delete the osnapy in /Applications (actually the entire /Applications/<application_name>.app )

    def _info_plist_substitute(self, info_plist_path):
        LOGGER.info('fixing up %s' % info_plist_path)
        tree = ElementTree.parse(info_plist_path)
        translations = {}

        # reverse-DNS format
        url_fields = self.url.split('.')
        if len(url_fields) != 3:
            LOGGER.error('URL "%s" improperly formatted - must be x.y.z' % self.url)
        reverse_dns_identifier = '%s.%s.%s' % (url_fields[-1], url_fields[-2], self.application_name)

        translations['CFBundleName'] = self.application_name
        translations['CFBundleDisplayName'] = self.application_name
        translations['CFBundleIdentifier'] = reverse_dns_identifier
        translations['CFBundleVersion'] = self.application_version
        translations['CFBundleShortVersionString'] = self.application_version
        translations['CFBundleSignature'] = url_fields[-2][0:4].upper()
        translations['NSHumanReadableCopyright'] = 'Copyright %s' % self.author
        next_translation = None
        for elem in tree.getiterator():
            if elem.tag == 'key' and elem.text in translations:
                next_translation = elem.text
            elif next_translation and elem.tag == 'string':
                LOGGER.debug('replaced', elem.tag, elem.text, translations[next_translation])
                elem.text = translations[next_translation]
                next_translation = None
        if False:
            for ds in tree.iterfind('dict'):
                print(ds.findtext('dict'))
                for d in ds:
                    print(d.findtext('key'))

        doctype = '<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">'
        with open(info_plist_path, 'w') as f:
            f.write(ElementTree.tostring(tree, xml_declaration=True, pretty_print=True, encoding='UTF-8',
                                         doctype=doctype).decode())

        return reverse_dns_identifier
