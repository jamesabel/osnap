import os
import sys

import osnap.const

from jinja2 import Template


def make_prkproj(application_name, pkgproj_path, verbose):
    template_file_path = os.path.join(os.path.dirname(sys.executable), '..', osnap.const.package_name,
                                      'template.pkgproj')
    if verbose:
        print('using %s as template' % template_file_path)
    with open(template_file_path) as template_file:
        template = Template(template_file.read())
        with open(pkgproj_path, 'w') as f:
            f.write(template.render(application_name=application_name))
