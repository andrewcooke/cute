
from os.path import join
from re import compile

CUTE_DIR = "/home/andrew/project/cute"
BLOG_DIR = "/home/andrew/project/www/cute"
BASE_URL = "http://www.acooke.org/cute/"
SHORT_URL = "http://acooke.org/cute/"
ABS_PATH = "/cute/"
N_RECENT = 10
N_REPLIES = 20
N_THREADS = 20
N_ALL = 100
N_MINI = 3
N_RSS = 10

PANDOC = "/usr/bin/pandoc"

TYPE_ARTICLE = 'article'
TYPE_REPLY = 'reply'

SCRIPTS_DIR = join(CUTE_DIR, 'src')
TEMPLATE_DIR = join(CUTE_DIR, 'templates')
CSS = join(TEMPLATE_DIR, 'compute.css')
DATA = join(TEMPLATE_DIR, 'data.html')
BODY = join(TEMPLATE_DIR, 'body.html')
REPLY = join(TEMPLATE_DIR, 'reply.html')
ABOUT = join(TEMPLATE_DIR, 'about.html')
INDEX = join(TEMPLATE_DIR, 'index.html')
SIDEBAR = join(TEMPLATE_DIR, 'sidebar.html')
MINIBAR = join(TEMPLATE_DIR, 'minibar.html')
CONTENTS = join(TEMPLATE_DIR, 'contents.html')
FEED = join(TEMPLATE_DIR, 'feed.png')
IMAGE = join(TEMPLATE_DIR, 'pancito.png')

PREV_FILE = join(BLOG_DIR, 'previous')
INDEX_FILE = join(BLOG_DIR, 'index.html')
SIDEBAR_FILE = join(BLOG_DIR, 'sidebar.html')
MINIBAR_FILE = join(BLOG_DIR, 'minibar.html')
CSS_FILE = join(BLOG_DIR, 'compute.css')
HTACCESS_FILE = join(BLOG_DIR, '.htaccess')
IMAGE_FILE = join(BLOG_DIR, 'pancito.png')
CONTENTS_FILE = join(BLOG_DIR, 'contents.html')
REPLY_FILE = join(BLOG_DIR, 'reply')
FEED_FILE = join(BLOG_DIR, 'rss2.xml')
LOCK_FILE = join(BLOG_DIR, '.lock')
# all these take an index
THREADS_FILE = join(BLOG_DIR, '.threads')  # links to recent articles
REPLIES_FILE = join(BLOG_DIR, '.replies')  # links to recent replies
RECENT_FILE = join(BLOG_DIR, '.recent')    # recent texts
ALL_FILE = join(BLOG_DIR, '.all')          # links to recent articles and replies
RSS_FILE = join(BLOG_DIR, '.rss')          # info for rss summary
TWEET_FILE = join(BLOG_DIR, '.tweet')      # 140 chars or less

HDR_SUBJECT = 'Subject'
HDR_FROM = 'From'
HDR_DATE = 'Date'
HDR_TO = 'To'
HDR_ENV = 'Envelope-to'
HDR_CC = 'Cc'
HDR_MARKDOWN = 'X-Markdown'

TPL_SUBJECT = 'title'
TPL_RAW_CONTENT = 'raw-content'
TPL_CONTENT = 'content'
TPL_PREVIOUS = 'previous'
TPL_PREV_ID = 'previous-id'
TPL_PREV_URL = 'previous-url'
TPL_NEXT = 'next'
TPL_ID = 'id'
TPL_URL = 'url'
TPL_FILENAME = 'filename'
TPL_REPLYTO = 'replyto'
TPL_FROM = 'from'
TPL_DATE = 'date'
TPL_THREADS = 'menu-threads'
TPL_REPLIES = 'menu-replies'
TPL_RECENT = 'recent'
TPL_PERMALINK = 'permalink'
TPL_REPLY = 'reply'
TPL_ANCHOR = 'anchor'
TPL_ANCHORLINK = 'anchorlink'
TPL_ALL = 'all'
TPL_SELF_AD = 'self-advert'

OLD_TAG = '[Cute]'
HTML = '.html'
PREVIOUS = 'Previous'
NEXT = 'Next'
PERMALINK = 'Permalink'
BAD_SUBJECTS = [compile(text) for text in [
    'confirm [a-f0-9]{10}', '^ *$', 'Bounce action', '^[Jj]oin$']]
BAD_FROM = compile("(>|&gt;)From")
GOOD_FROM = 'From'
LINK = compile("((?:https?|ftp)://[^ \n\t\r\(\)<>\"']*)")
EMAIL = compile("<?(\w+)@[\w\.]+>?")
MARKER = compile(r'^\s*<!--\s+([\w\-]+)\s+-->\s*$')
ADDRESS = compile(r'compute[+\-](\w+)@acooke.org')
TIME = compile(r'^([^+\-]*)([+\-]\d\d\d\d)?(.*)$')
MAX_DESCR = 400

SELF_AD = '''
<h3>Personal Projects</h3>
<p><a href="/portfolio/lepl">Lepl</a> parser for Python.</p>
<p><a href="http://colorlessgreen.net">Colorless Green</a>.</p>
<p><a href="/photography">Photography</a> around Santiago.</p>
<p><a href="/portfolio/practicl">SVG</a> experiment.</p>
<h3>Professional Portfolio</h3>
<p><a href="/portfolio/seismic-cal">Calibration</a> of seismometers.
<p><a href="/portfolio/data-access">Data</a> access via web services.
<p><a href="/portfolio/cache">Cache</a> rewrite.
<p>Extending <a href="/portfolio/security">OpenSSH</a>.
'''

URL_REWRITES = dict([
('http://www.acooke.org/andrew/compute.html', 'http://www.acooke.org/cute'),
('http://www.acooke.org/andrew', 'http://www.acooke.org'),
('http://www.acooke.org/andrew/papers/index.html#esoa', 'http://www.acooke.org/esoa.pdf'),
('http://www.acooke.org/andrew/papers/index.html#impl', 'http://www.acooke.org/esoa.pdf'),
('http://www.acooke.org/andrew/papers/tiny.pdf', 'http://www.acooke.org/tiny.pdf'),
('http://www.acooke.org/andrew/papers/index.html#schema', 'http://www.acooke.org/schema.pdf'),
('http://www.acooke.org/andrew/papers/index.html', 'http://www.acooke.org'),
('http://www.acooke.org/andrew/papers/booklet.pdf', 'http://www.acooke.org/booklet.pdf'),
('http://www.acooke.org/andrew/papers/lazy.pdf', 'http://www.acooke.org/lazy.pdf'),
('http://www.acooke.org/andrew/papers/vocab.pdf', 'http://www.acooke.org/vocab.pdf'),
('http://www.acooke.org/andrew/papers/impl.pdf', 'http://www.acooke.org/impl.pdf'),
('http://www.acooke.org/andrew/papers/esoa.pdf', 'http://www.acooke.org/esoa.pdf'),
('http://www.acooke.org/andrew/writing/compgeneral.html#agile', 'http://www.acooke.org/agile-review.html'),
('http://www.acooke.org/andrew/writing/minimal/static.html', 'http://www.acooke.org/minimal/background.html'),
('http://www.acooke.org/andrew/writing/minimal/dynamic.html', 'http://www.acooke.org/minimal'),
('http://www.acooke.org/andrew/index.html', 'http://www.acooke.org'),
('http://www.acooke.org/andrew/writing/arms.html', 'http://www.acooke.org/arms.html')
])
