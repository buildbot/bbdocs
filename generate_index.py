#!/usr/bin/env python3

import re
import os

import packaging.version
from jinja2 import Environment, FileSystemLoader

PATH = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_ENVIRONMENT = Environment(
    autoescape=False,
    loader=FileSystemLoader(PATH),
    trim_blocks=False)


def render_template(template_filename, context):
    return TEMPLATE_ENVIRONMENT.get_template(template_filename).render(context)


def version_part_parse(part):
    if not part:
        return 0
    return int(part)


def version_parse(version) -> packaging.version.Version:
    try:
        return packaging.version.parse(version)
    except packaging.version.InvalidVersion:
        pass
    # packaging.version.parse does not parse some of the existing version numbers
    version = version.replace("p", "post")
    return packaging.version.parse(version)


def create_index_html():
    fname = "docs/index.html"
    versions = []
    for fn in os.listdir('docs'):
        m = re.match(r'^\d\..*', fn)
        if m is not None:
            v = version_parse(fn)
            if v.is_prerelease or v.is_devrelease:
                continue
            if v > version_parse("0.8.5"):
                versions.append((v, fn))
    versions.sort(reverse=True)
    current_version = versions[0][1]
    os.system("find docs/{} -name '*.html' | xargs python3 add-tracking.py".format(current_version))
    os.system("rm -f docs/current")
    os.system("ln -sf {} docs/current".format(current_version))
    older_versions = versions[1:]
    context = {
        'current_version': current_version,
        'older_versions': older_versions,
    }
    #
    with open(fname, 'w') as f:
        html = render_template('index.html.j2', context)
        f.write(html)


def main():
    create_index_html()

########################################

if __name__ == "__main__":
    main()
