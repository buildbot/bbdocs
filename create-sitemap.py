import os

BASE_URL = 'http://buildbot.net/buildbot/'

def find(dir, exclude=[]):
    for (dirpath, dirnames, filenames) in os.walk(dir):
        for excl in exclude:
            if excl in dirnames:
                del dirnames[dirnames.index(excl)]
        for fn in filenames:
            yield os.path.join(dirpath, fn)

def process(baseurl, dir, f):
    if dir.endswith('/current'):
        priority = 1.0
    elif dir.endswith('/latest'):
        priority = 0.7
    else:
        priority = 0.5

    for filename in find(dir, exclude='reference _static _sources'.split()):
        ignored = False
        for ignore in 'search.html .buildinfo objects.inv searchindex.js full.html'.split():
            if ignore in filename:
                ignored = True
                break
        if not ignored:
            f.write("<url><loc>%s%s</loc><priority>%s</priority></url>\n" % (baseurl, filename, priority))

dirs = [ 'docs/%s' % x for x in os.listdir('docs') ]
dirs = [ x for x in dirs if os.path.isdir(x) and not os.path.islink(x) ]
dirs += [ 'docs/current', 'docs/latest' ]

f = open('sitemap.xml', 'w')
f.write("""\
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
""")
for dir in dirs:
    process(BASE_URL, dir, f)
f.write("""\
</urlset>
""")
f.close()

if os.stat('sitemap.xml').st_size > 10*1024*1024:
    print "sitemap.xml is too bug (greater than 10MB)"
