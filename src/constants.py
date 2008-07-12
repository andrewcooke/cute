
from os.path import join
from re import compile

CUTE_DIR = "/home/andrew/projects/personal/src/python/cute"
BLOG_DIR = "/home/andrew/projects/personal/www-new/blog"
BASE_URL = "http://www.acooke.org/blog/"
N_RECENT = 10
N_REPLIES = 20
N_THREADS = 20

SCRIPTS_DIR = join(CUTE_DIR, 'src')
TEMPLATE_DIR = join(CUTE_DIR, 'templates')
CSS = join(TEMPLATE_DIR, 'compute.css')
DATA = join(TEMPLATE_DIR, 'data.html')
BODY = join(TEMPLATE_DIR, 'body.html')
ABOUT = join(TEMPLATE_DIR, 'about.html')
INDEX = join(TEMPLATE_DIR, 'index.html')
CONTENTS = join(TEMPLATE_DIR, 'contents.html')
FEED = join(TEMPLATE_DIR, 'feed.png')
BG_IMAGE = join(TEMPLATE_DIR, 'pancito.png')

PREV_FILE = join(BLOG_DIR, 'previous')
INDEX_FILE = join(BLOG_DIR, 'index.html')
# all these take an index
THREADS_FILE = join(BLOG_DIR, 'threads')
REPLIES_FILE = join(BLOG_DIR, 'replies')
RECENT_FILE = join(BLOG_DIR, 'recent')

HDR_SUBJECT = 'Subject'
HDR_FROM = 'From'
HDR_DATE = 'Date'

TPL_SUBJECT = 'title'
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

OLD_TAG = '[Cute]'
HTML = '.html'
PREVIOUS = 'Previous'
NEXT = 'Next'
PERMALINK = 'Permalink'
BAD_SUBJECTS = [compile(text) for text in [
    'confirm [a-f0-9]{10}', '^ *$', 'Bounce action', '^[Jj]oin$']]
BAD_FROM = compile(">From")
GOOD_FROM = 'From'
BAD_CUTE = compile("http://www.acooke.org/andrew/cute")
GOOD_CUTE = 'http://www.acooke.org/blog'
LINK = compile("(http://[^ \n\t\r\(\)<>]*)")
EMAIL = compile("<?(\w+)@[\w\.]+>?")
MARKER = compile(r'^\s*<!--\s+([\w\-]+)\s+-->\s*$')
