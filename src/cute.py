from datetime import datetime
from email import message_from_binary_file
from logging import getLogger
from os import mkdir, listdir
from os.path import exists, join as pjoin
from re import sub
from subprocess import Popen, PIPE
from sys import stderr
from time import strptime

from PyRSS2Gen import RSSItem, Guid, RSS2

from constants import *

log = getLogger(__name__)


def get_time(path):
    with open(path, 'rb') as source:
        email = message_from_binary_file(source)
        if email[HDR_DATE]:
            return time_from_date(email[HDR_DATE])
        else:
            raise BadTime()


def _time_from_date(date):
    match = TIME.match(date)
    if not match:
        raise IOError(date)
    date = match.group(1) + match.group(3)
    date = date.strip()
    try:
        if match.group(3):
            return strptime(date, '%a, %d %b %Y %H:%M:%S  (%Z)')
        else:
            return strptime(date, '%a, %d %b %Y %H:%M:%S')
    except:
        return strptime(match.group(1).strip(), '%a, %d %b %Y %H:%M:%S')


def time_from_date(date):
    try:
        from dateutil.parser import parse
        return parse(date).timetuple()
    except Exception as e:
        log.warning(f'dateutil failed for {date}: {e}')
        return _time_from_date(date)


def create_blog_dir():
    if not exists(BLOG_DIR):
        mkdir(BLOG_DIR)


def read_single_line(path, default=None):
    try:
        with open(path) as source:
            return source.readline()
    except:
        if default is not None:
            return default
        else:
            raise


def read_file(path, default=None):
    try:
        with open(path) as source:
            return source.read()
    except:
        if default is not None:
            return default
        else:
            raise


def write_single_line(text, path):
    with open(path, 'w') as destn:
        destn.write(text)


def write_rss(map):
    with open(RSS_FILE + str(0), 'w') as destn:
        # first line is title
        destn.write(map[TPL_SUBJECT] + '\n')
        # second line is url
        destn.write(map[TPL_URL] + '\n')
        # third line is date
        destn.write(str(list(time_from_date(map[TPL_DATE]))) + '\n')
        # rest is description
        content = map[TPL_RAW_CONTENT]
        if len(content) > MAX_DESCR:
            content = content[0:MAX_DESCR] + '...'
        destn.write(content)


def write_tweet(map):
    with open(TWEET_FILE, 'w') as destn:
        msg = SHORT_URL + map[TPL_URL]
        msg = msg + ' ' + map[TPL_SUBJECT]
        while len(msg) > 138:
            msg = msg[0:msg.rindex(' ')]
        destn.write(msg)


def read_rss():
    rss = []
    count = 0
    while exists(RSS_FILE + str(count)):
        with open(RSS_FILE + str(count)) as source:
            title = source.readline()
            url = source.readline()
            date = eval(source.readline())
            description = ''.join(source.readlines())
            rss.append(RSSItem(
                title=title,
                link=BASE_URL + url,
                description=description,
                guid=Guid(url),
                pubDate=datetime(*date[0:5])))
        count = count + 1
    return rss


def read_all(path, join='', max_count=-1):
    text = []
    count = 0
    while exists(path + str(count)) and count != max_count:
        with open(path + str(count)) as source:
            text.append(source.read())
        count = count + 1
    return join.join(text)


def is_indent(line):
    return not line or line[0] == ' '


def by_indent(lines):
    block = []
    blocks = [block]
    old_indent = is_indent(lines[0])
    for line in lines:
        new_indent = is_indent(line)
        if new_indent == old_indent:
            block.append(line)
        else:
            block = [line]
            blocks.append(block)
            old_indent = new_indent
    return blocks


def join_indents(old_blocks):
    new_blocks = []
    for block in old_blocks:
        if not new_blocks:
            new_blocks.append(block)
        else:
            if is_indent(block[0]) and is_indent(new_blocks[-1][0]):
                new_blocks[-1].extend(block)
            else:
                new_blocks.append(block)
    return new_blocks


def add_tag(lines):
    if is_indent(lines[0]):
        tag = "pre"
    else:
        tag = "p"
    return "<%s>%s</%s>" % (tag, '\n'.join(lines), tag)


def unpack(message):
    payload = message.get_payload()
    if message.is_multipart():
        return unpack(payload[0])
    else:
        return payload


def unpack_charset(email):
    if email[HDR_CTYPE]:
        ctype = email[HDR_CTYPE]
        match = CTYPE.search(ctype)
        if match: return match.group(1)
    return 'latin-1'


def linkify(match):
    url = match.group(1)
    if url in URL_REWRITES: url = URL_REWRITES[url]
    return "<a href='%s'>%s</a>" % (url, url)


def format_raw(text):
    if text:
        text = text.strip()
        text = sub('<', '&lt;', text)
        text = sub('>', '&gt;', text)
        text = sub(BAD_FROM, GOOD_FROM, text)
        text = sub(LINK, linkify, text)
        text = sub(EMAIL, lambda match: match.group(1) + "@...", text)
    else:
        text = ''
    return text


def format_pre(text):
    return '<pre>' + format_raw(text) + '</pre>'


def format_md(text):
    p = Popen([PANDOC, '--from=markdown', '--to=html', '--mathjax'],
              stdin=PIPE, stdout=PIPE)
    return p.communicate(text.encode('utf-8'))[0].decode('utf-8')


def format(email, text):
    if HDR_MARKDOWN in email:
        return format_md(text)
    else:
        return format_pre(text)


def build_map(email, exists=False):
    map = {}
    map[TPL_SUBJECT] = sub('[\n\r]', ' ', format_raw(email[HDR_SUBJECT]))
    map[TPL_FROM] = format_raw(email[HDR_FROM])
    map[TPL_DATE] = email[HDR_DATE]
    raw = unpack(email)
    map[TPL_RAW_CONTENT] = raw
    map[TPL_CONTENT] = format(email, map[TPL_RAW_CONTENT])
    map[TPL_PREV_ID] = read_single_line(PREV_FILE, '')
    if map[TPL_PREV_ID]:
        map[TPL_PREV_URL] = map[TPL_PREV_ID] + SHTML
        map[TPL_PREVIOUS] = '<a href="%s">%s</a>' % (map[TPL_PREV_URL], PREVIOUS)
    map[TPL_SELF_AD] = SELF_AD
    generate_id(map, email, exists)
    generate_url(map, exists)
    map[TPL_PERMALINK] = "<a href='%s'>%s</a>" % (map[TPL_URL], PERMALINK)
    map[TPL_FILENAME] = pjoin(BLOG_DIR, map[TPL_ID] + SHTML)
    map[TPL_REPLYTO] = "<a href='mailto:compute+%(id)s@acooke.org'>Comment on this post</a>" % map
    if map[TPL_SUBJECT] and map[TPL_SUBJECT].startswith(OLD_TAG):
        map[TPL_SUBJECT] = map[TPL_SUBJECT][len(OLD_TAG):]
    return map


def generate_url(map, exists):
    map[TPL_URL] = map[TPL_ID] + SHTML
    if exists:
        map[TPL_ANCHOR] = sub('\W', '', map[TPL_DATE])
        map[TPL_ANCHORLINK] = "<a id='%s'></a>" % map[TPL_ANCHOR]
        map[TPL_URL] = map[TPL_URL] + '#' + map[TPL_ANCHOR]


def generate_id(map, email, exists):
    if exists:
        map[TPL_ID] = generate_old_id(map, email)
    else:
        map[TPL_ID] = generate_new_id(map)


def address_from(header):
    match = ADDRESS.search(header)
    if match:
        return match.group(1)
    else:
        return None


def generate_old_id(map, email):
    to = address_from(email[HDR_TO])
    if not to and email[HDR_ENV]: to = address_from(email[HDR_ENV])
    if not to and email[HDR_CC]: to = address_from(email[HDR_CC])
    if not to and email[HDR_TO]: to = address_from(email[HDR_TO])
    if not to:
        raise IOError('no suitable destination address')
    destn = join(BLOG_DIR, to + SHTML)
    if exists(destn):
        return to
    for file in listdir(BLOG_DIR):
        if file.endswith(SHTML):
            file = file[0:-+len(SHTML)]
            if to.lower() == file.lower():
                return file
    raise BadSubject('no match for ' + to)


def generate_new_id(map):
    subject = map[TPL_SUBJECT]
    if subject:
        if subject.startswith(OLD_TAG):
            subject = subject[len(OLD_TAG):]
        match = TAGS.match(subject)
        if match:
            subject = match.group(1)
        subject = NOT_ALPHAS.sub('', subject)
        if (len(subject) > 10):
            subject = subject[0:10]
        count = 0
        existing = set(file.lower() for file in listdir(BLOG_DIR))
        while (subject + str(count) + SHTML).lower() in existing:
            count = count + 1
        return subject + str(count)
    else:
        return ''


def skip(map):
    subject = map[TPL_SUBJECT]
    if not subject:
        return True
    for regexp in BAD_SUBJECTS:
        if regexp.search(subject):
            return True
    return False


def do_template(map, in_filename, out_filename):
    text = ''
    with open(in_filename) as source:
        for line in source.readlines():
            match = MARKER.search(line)
            if match:
                name = match.group(1).lower()
                if name in map:
                    line = map[name] + "\n"
            text = text + line
    with open(out_filename, 'w') as destn:
        destn.write(text)


def shuffle_stored(path, count, down=True):
    if down:
        for n in range(count, 0, -1):
            source = path + str(n - 1)
            destn = path + str(n)
            copy(source, destn, force=True)
    else:
        for n in range(count):
            source = path + str(n + 1)
            destn = path + str(n)
            copy(source, destn, force=True)


def copy(spath, dpath, force=False):
    if exists(spath):
        if force or not exists(dpath):
            with open(spath) as source:
                contents = source.readlines()
            with open(dpath, 'w') as destn:
                destn.writelines(contents)


def update_sidebar(map):
    shuffle_stored(ALL_FILE, N_ALL)
    write_single_line("<a href='%s%s' target='_top'>%s</a>" %
                      (ABS_PATH, map[TPL_URL], map[TPL_SUBJECT]),
                      ALL_FILE + str(0))
    do_template({TPL_ALL: read_all(ALL_FILE, join=';\n')},
                SIDEBAR, SIDEBAR_FILE)
    do_template({TPL_ALL: read_all(ALL_FILE, join='\n</li><li>\n',
                                   max_count=3)},
                MINIBAR, MINIBAR_FILE)


def update_rss(items):
    rss = RSS2(
        title="C[omp]ute",
        link=BASE_URL,
        description="Andrew Cooke's blog",
        lastBuildDate=datetime.now(),
        items=items)
    with open(FEED_FILE, 'w') as destn:
        rss.write_xml(destn)


def add_new_entry(email):
    create_blog_dir()
    map = build_map(email)
    if not skip(map):
        # generate post (ie the permalink page)
        do_template(map, DATA, map[TPL_FILENAME])
        stderr.write('writing %s\n' % map[TPL_FILENAME])
        if map[TPL_PREV_ID]:
            # update the "next" link in the previous entry
            next = "<a href='%s'>%s</a>" % (map[TPL_ID] + SHTML, NEXT)
            prev = pjoin(BLOG_DIR, map[TPL_PREV_ID] + SHTML)
            do_template({TPL_NEXT: next}, prev, prev)
        # save current file name so we can update next there next time
        write_single_line(map[TPL_ID], PREV_FILE)
        # generate main page
        do_template(map, INDEX, INDEX_FILE)
        # update contents
        copy(CONTENTS, CONTENTS_FILE)
        do_template({TPL_CONTENT:
                         "<!-- CONTENT -->\n<li><a href='%s'>%s</a></li>" %
                         (map[TPL_URL], map[TPL_SUBJECT]),
                     TPL_SELF_AD: SELF_AD},
                    CONTENTS_FILE, CONTENTS_FILE)
        # add previous entries, without reprocessing
        update = {}
        update[TPL_RECENT] = read_all(RECENT_FILE)
        update[TPL_THREADS] = read_all(THREADS_FILE)
        update[TPL_REPLIES] = read_all(REPLIES_FILE)
        do_template(update, INDEX_FILE, INDEX_FILE)
        # shuffle the saved entries
        shuffle_stored(RECENT_FILE, N_RECENT)
        # add a new saved entry to include in the main page
        do_template(map, BODY, RECENT_FILE + str(0))
        # same for threads links
        shuffle_stored(THREADS_FILE, N_THREADS)
        write_single_line("<p><a href='%s'>%s</a></p>\n" %
                          (map[TPL_URL], map[TPL_SUBJECT]),
                          THREADS_FILE + str(0))
        # same for rss records
        shuffle_stored(RSS_FILE, N_RSS)
        write_rss(map)
        try:
            update_rss(read_rss())
        except UnicodeDecodeError as e:
            log.warning(e)
            # delete the last rss entry
            shuffle_stored(RSS_FILE, N_RSS, down=False)
        # and tweet
        write_tweet(map)
        # update sidebar
        update_sidebar(map)
        # copy files on first article
        copy(CSS, CSS_FILE)
        copy(IMAGE, IMAGE_FILE)


def add_reply(email):
    map = build_map(email, exists=True)
    if not skip(map):
        do_template(map, REPLY, REPLY_FILE)
        reply = {TPL_REPLY: read_file(REPLY_FILE)}
        # restrict front page reply to the main article
        line = read_single_line(THREADS_FILE + str(0), '')
        if line.find("'" + map[TPL_ID] + SHTML + "'") > -1:
            do_template(reply, INDEX_FILE, INDEX_FILE)
        post = join(BLOG_DIR, map[TPL_ID] + SHTML)
        do_template(reply, post, post)
        shuffle_stored(REPLIES_FILE, N_REPLIES)
        write_single_line("<p><a href='%s'>%s</a></p>\n" %
                          (map[TPL_URL], map[TPL_SUBJECT]),
                          REPLIES_FILE + str(0))
        update_sidebar(map)


class Multipart(IOError):
    pass


class BadSubject(IOError):
    pass


class BadTime(IOError):
    pass
