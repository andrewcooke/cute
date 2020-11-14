
from os.path import join
from re import compile

CUTE_DIR = "/home/andrew/project/cute"
BLOG_DIR = "/home/andrew/project/www/cute"
BASE_URL = "https://www.acooke.org/cute/"
SHORT_URL = "https://acooke.org/cute/"
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
HDR_CTYPE = 'Content-Type'

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
SHTML = '.shtml'
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
CTYPE = compile(r'charset=(\S+)')
TAGS = compile(r'\s*\[[^\]]+\](.*)')
NOT_ALPHAS = compile(r'[^a-z0-9A-Z]')
MAX_DESCR = 400

SELF_AD = '''
<h3>Personal Projects</h3>
<p><a href="https://github.com/andrewcooke/choochoo">Choochoo</a> Training Diary</p>
'''

URL_REWRITES = dict([
('http://www.acooke.org/andrew', 'http://www.acooke.org'),
('http://www.acooke.org/andrew/index.html', 'http://www.acooke.org')
])
