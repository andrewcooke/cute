
from __future__ import with_statement
from os import mkdir, listdir
from os.path import exists, join as pjoin
from re import compile, sub
from sys import stderr
from string import join as sjoin

from constants import *


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
            raise sys.exc_info()

def read_file(path, default=None):
    try:
        with open(path) as source:
            return sjoin(source.readlines(), '')
    except:
        if default is not None:
            return default
        else:
            raise sys.exc_info()

def write_single_line(text, path):
    with open(path, 'w') as destn:
        destn.write(text)

def read_all(path):
    text = []
    count = 0
    while exists(path + str(count)):
        with open(path + str(count)) as source:
            text.extend(source.readlines())
        count = count + 1
    return sjoin(text, '')

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

def by_blank_lines(lines):
    blocks = []
    prev_line_blank = True
    for line in lines:
        if len(line.strip()) == 0:
            prev_line_blank = True
        else:
            if prev_line_blank:
                block = []
                blocks.append(block)
            block.append(line)
            prev_line_blank = False
    return blocks

def join_indents(old_blocks):
    new_blocks=[]
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
    return "<%s>%s</%s>" % (tag, sjoin(lines, '\n'), tag)

def unpack(payload):
    if isinstance(payload, basestring):
        return payload
    else:
        raise Multipart('multipart message')

def un_html(text):
    text = sub('<', '&lt;', text)
    text = sub('>', '&gt;', text)
    return text

def format(text):
    text = un_html(text).strip()
    return '<pre>' + text + '</pre>'
    # no longer try to format text
#    blocks1 = []
#    for block in by_blank_lines(text.splitlines()):
#        blocks1.extend(by_indent(block))
#    blocks2 = []
#    for block in join_indents(blocks1):
#        blocks2.append([un_html(line) for line in block])
#    return sjoin([add_tag(block) for block in blocks2], "\n")

def build_map(email, exists=False):
    map = {}
    map[TPL_SUBJECT] = email[HDR_SUBJECT]
    map[TPL_FROM] = email[HDR_FROM]
    map[TPL_DATE] = email[HDR_DATE]
    map[TPL_CONTENT] = format(unpack(email.get_payload()))
    map[TPL_PREV_ID] = read_single_line(PREV_FILE, '')
    if map[TPL_PREV_ID]:
        map[TPL_PREV_URL] = map[TPL_PREV_ID] + HTML
        map[TPL_PREVIOUS] = '<a href="%s">%s</a>' % (map[TPL_PREV_URL], PREVIOUS)
    generate_id(map, email, exists)
    generate_url(map, exists)
    map[TPL_PERMALINK] = "<a href='%s'>%s</a>" % (map[TPL_URL], PERMALINK)
    map[TPL_FILENAME] = pjoin(BLOG_DIR, map[TPL_ID] + HTML)
    map[TPL_REPLYTO] = "<a href='mailto:compute-%(id)s delete-this curly-at acooke dot org'>Comment on this post</a>" % map
    if map[TPL_SUBJECT] and map[TPL_SUBJECT].startswith(OLD_TAG):
         map[TPL_SUBJECT] =  map[TPL_SUBJECT][len(OLD_TAG):]
    return map

def generate_url(map, exists):
    map[TPL_URL] = map[TPL_ID] + HTML
    if exists:
        map[TPL_ANCHOR] = sub('\W', '', map[TPL_DATE])
        map[TPL_ANCHORLINK] = "<a id='%s'/>" % map[TPL_ANCHOR]
        map[TPL_URL] = map[TPL_URL] + '#' + map[TPL_ANCHOR]

def generate_id(map, email, exists):
    if exists:
        map[TPL_ID] = generate_old_id(map, email)
    else:
        map[TPL_ID] = generate_new_id(map)

def address_from(header):
    match = ADDRESS.match(header)
    if match:
        return match.group(1)
    else:
        return None

def generate_old_id(map, email):
    to = address_from(email[HDR_TO])
    if not to: to = address_from(email[HDR_ENV])
    if not to: to = address_from(email[HDR_CC])
    if not to:
        raise IOError('no suitable destination address')
    destn = join(BLOG_DIR, to + HTML)
    if exists(destn):
        return to
    for file in listdir(BLOG_DIR):
        if file.endswith(HTML):
            file = file[0:-5]
            if to.lower() == file.lower():
                return file
    raise BadSubject('no match for ' + to)

def generate_new_id(map):
    subject = map[TPL_SUBJECT]
    if subject:
        if subject.startswith(OLD_TAG):
            subject = subject[len(OLD_TAG):]
        not_alphas = compile(r'[^a-z0-9A-Z]')
        subject = not_alphas.sub('', subject)
        if (len(subject) > 10):
            subject = subject[0:10]
        count = 0
        while exists(pjoin(BLOG_DIR, subject + str(count) + HTML)):
            count = count + 1
        return subject + str(count)
    else:
        return ''

def skip(map):
    subject = map[TPL_SUBJECT]
    if not subject: return True
    for regexp in BAD_SUBJECTS:
        if regexp.search(subject): return True
    return False

def linkify(match):
    return "<a href='%s'>%s</a>" % (match.group(1), match.group(1))

def fixup(line):
    line = sub(BAD_FROM, GOOD_FROM, line)
    line = sub(BAD_CUTE, GOOD_CUTE, line)
    line = sub(LINK, linkify, line)
    line = sub(EMAIL, lambda match: match.group(1) + "@...", line)
    return line

def do_template(map, in_filename, out_filename, fix=True):
    first = True
    with open(in_filename) as source:
        for line in source.readlines():
            if first:
                first = False
                text = line
            else:
                match = MARKER.search(line)
                if match:
                    name = match.group(1).lower()
                    if name in map:
                        line = map[name] + "\n"
                if fix:
                    text = text + fixup(line)
                else:
                    text = text + line
    with open(out_filename, 'w') as destn:
        destn.write(text)

def shuffle_stored(path, count):
    for n in range(count, 0, -1):
        source = path + str(n-1)
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
    write_single_line("<p><a href='%s'>%s</a></p>\n" % 
                      (map[TPL_URL], map[TPL_SUBJECT]), 
                      ALL_FILE + str(0))
    do_template({TPL_ALL: read_all(ALL_FILE)},
                SIDEBAR, SIDEBAR_FILE, fix=False)

def add_new_entry(email):
    create_blog_dir()
    map = build_map(email)
    if not skip(map):
        # generate post (ie the permalink page)
        do_template(map, DATA, map[TPL_FILENAME])
        stderr.write('writing %s\n' %  map[TPL_FILENAME])
        if map[TPL_PREV_ID]:
            # update the "next" link in the previous entry
            next = "<a href='%s'>%s</a>" % (map[TPL_ID] + HTML, NEXT)
            prev = pjoin(BLOG_DIR, map[TPL_PREV_ID] + HTML)
            do_template({TPL_NEXT: next}, prev, prev, fix=False)
        # save current file name so we can update next there next time
        write_single_line(map[TPL_ID], PREV_FILE)
        # generate main page
        do_template(map, INDEX, INDEX_FILE)
        # update contents
        copy(CONTENTS, CONTENTS_FILE)
        do_template({TPL_CONTENT: 
                     "<!-- CONTENT -->\n<li><a href='%s'>%s</a></li>" %
                     (map[TPL_URL], map[TPL_SUBJECT])},
                    CONTENTS_FILE, CONTENTS_FILE, fix=False)
        # add previous entries, without reprocessing
        update = {}
        update[TPL_RECENT] = read_all(RECENT_FILE)
        update[TPL_THREADS] = read_all(THREADS_FILE)
        update[TPL_REPLIES] = read_all(REPLIES_FILE)
        do_template(update, INDEX_FILE, INDEX_FILE, fix=False)
        # shuffle the saved entries
        shuffle_stored(RECENT_FILE, N_RECENT)
        # add a new saved entry to include in the main page
        do_template(map, BODY, RECENT_FILE + str(0))
        # same for threads links
        shuffle_stored(THREADS_FILE, N_THREADS)
        write_single_line("<p><a href='%s'>%s</a></p>\n" % 
                          (map[TPL_URL], map[TPL_SUBJECT]), 
                          THREADS_FILE + str(0))
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
        do_template(reply, INDEX_FILE, INDEX_FILE, fix=False)
        post = join(BLOG_DIR, map[TPL_ID] + HTML)
        do_template(reply, post, post, fix=False)
        shuffle_stored(REPLIES_FILE, N_REPLIES)
        write_single_line("<p><a href='%s'>%s</a></p>\n" % 
                          (map[TPL_URL], map[TPL_SUBJECT]), 
                          REPLIES_FILE + str(0))
        update_sidebar(map)

class Multipart(IOError):
    pass

class BadSubject(IOError):
    pass
