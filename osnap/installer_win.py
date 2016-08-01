
import os
import datetime
import collections
import subprocess

import osnap.make_nsis


def create_installer_win(author, application_name, description, url, project_packages, verbose):

    nsis_file_name = application_name + '.nsis'
    exe_name = application_name + '.exe'

    defines = collections.OrderedDict()
    defines['COMPANYNAME'] = author
    defines['APPNAME'] = application_name
    defines['EXENAME'] = exe_name
    defines['DESCRIPTION'] = '"' + description + '"'  # the description must be in quotes

    import _build_

    s = int(_build_.seconds_since_epoch)
    dt = datetime.datetime.fromtimestamp(s)
    defines['VERSIONMAJOR'] = dt.year
    defines['VERSIONMINOR'] = dt.timetuple().tm_yday
    defines['VERSIONBUILD'] = _build_.version

    # These will be displayed by the "Click here for support information" link in "Add/Remove Programs"
    # It is possible to use "mailto:" links in here to open the email client
    defines['HELPURL'] = url  # "Support Information" link
    defines['UPDATEURL'] = url  # "Product Updates" link
    defines['ABOUTURL'] = url  # "Publisher" link

    if verbose:
        print('writing %s' % nsis_file_name)
    nsis = osnap.make_nsis.MakeNSIS(defines, nsis_file_name, project_packages)
    nsis.write_all()
    subprocess.check_call([os.path.join('c:', os.sep, 'Program Files (x86)', 'NSIS', 'makensis'), nsis_file_name])