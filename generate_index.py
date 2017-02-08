#!/usr/bin/env python

import os

from jinja2 import Environment, FileSystemLoader
from packaging import version

PATH = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_ENVIRONMENT = Environment(
    autoescape=False,
    loader=FileSystemLoader(PATH),
    trim_blocks=False)


def render_template(template_filename, context):
    return TEMPLATE_ENVIRONMENT.get_template(template_filename).render(context)


def create_index_html():
    fname = "docs/index.html"
    versions = []
    for fn in os.listdir('docs'):
        if fn.startswith('0.'):
            v = version.parse(fn)
            if v > version.parse("0.8.5"):
                versions.append((v, fn))
    versions.sort(reverse=True)
    current_version = versions[0][1]
    os.system("find docs/{} -name '*.html' | xargs python add-tracking.py".format(current_version))
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
