import re, textwrap, sys

subre = re.compile("(<!-- GA-TRACKING-START.*GA-TRACKING-END -->\\s*)?</head>", re.S)
def process(filename):
    data = open(filename).read()

    data = subre.sub(textwrap.dedent("""\
        <!-- GA-TRACKING-START -->
        <script type="text/javascript">
        var gaJsHost = (("https:" == document.location.protocol) ? "https://ssl." : "http://www.");
        document.write(unescape("%3Cscript src='" + gaJsHost + "google-analytics.com/ga.js' type='text/javascript'%3E%3C/script%3E"));
        </script>
        <script type="text/javascript">
        try{
        var pageTracker = _gat._getTracker("UA-12313843-4");
        pageTracker._setDomainName("none");
        pageTracker._setAllowLinker(true);
        pageTracker._trackPageview();
        } catch(err) {}
        </script>
        <!-- GA-TRACKING-END -->
        </head>"""), data)

    open(filename, "w").write(data)

for i in sys.argv[1:]:
    process(i)
