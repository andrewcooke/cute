
from __future__ import with_statement
from os import mkdir
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

def indent(line):
    for i in range(len(line)):
        if line[i] != ' ':
            return i
    return 0

def by_indent(lines):
    block = []
    blocks = [block]
    old_indent = indent(lines[0])
    for line in lines:
        new_indent = indent(line)
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

def add_tag(lines):
    if indent(lines[0]) > 0:
        tag = "pre"
    else:
        tag = "p"
    return "<%s>%s</%s>" % (tag, sjoin(lines, '\n'), tag)

def format(text):
    blocks = []
    for block in by_blank_lines(text.splitlines()):
        blocks.extend(by_indent(block))
    return sjoin([add_tag(block) for block in blocks], "\n")

def build_map(email):
    map = {}
    map[TPL_SUBJECT] = email[HDR_SUBJECT]
    map[TPL_FROM] = email[HDR_FROM]
    map[TPL_DATE] = email[HDR_DATE]
    map[TPL_CONTENT] = format(email.get_payload())
    map[TPL_PREV_ID] = read_single_line(PREV_FILE, '')
    if map[TPL_PREV_ID]:
        map[TPL_PREV_URL] = map[TPL_PREV_ID] + HTML
        map[TPL_PREVIOUS] = '<a href="%s">%s</a>' % (map[TPL_PREV_URL], PREVIOUS)
    map[TPL_ID] = generate_id(map)
    map[TPL_URL] = map[TPL_ID] + HTML
    map[TPL_PERMALINK] = '<a href="%s">%s</a>' % (map[TPL_URL], PERMALINK)
    map[TPL_FILENAME] = pjoin(BLOG_DIR, map[TPL_ID] + HTML)
    map[TPL_REPLYTO] = '<a href=\"mailto:compute-%(id)s delete-this curly-at acooke dot org\">Comment on this post</a>' % map
    return map

def generate_id(map):
    subject = map[TPL_SUBJECT]
    if subject.startswith(OLD_TAG):
        subject = subject[len(OLD_TAG):]
    not_alphas = compile(r'[^a-z0-9A-Z]')
    subject = not_alphas.sub('', subject)
    if (len(subject) > 10):
        subject = subject[0:10]
    subject = subject.upper()
    count = 0
    while exists(pjoin(BLOG_DIR, subject + str(count) + HTML)):
        count = count + 1
    return subject + str(count)

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
    text = ""
    with open(in_filename) as source:
        for line in source.readlines():
            match = MARKER.search(line)
            if match:
                name = match.group(1).lower()
                if name in map:
                    line = map[name] + "\n"
                else:
                    print 'no value for', name
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
        if exists(source):
            # todo - a real copy here
            do_template({}, source, destn, fix=False)

def add_new_entry(email):
    create_blog_dir()
    map = build_map(email)
    if not skip(map):
        # generate post (ie the permalink page)
        do_template(map, DATA, map[TPL_FILENAME])
        if map[TPL_PREV_ID]:
            # update the "next" link in the previous entry
            next = "<a href='%s'>%s</a>" % (map[TPL_ID] + HTML, NEXT)
            prev = pjoin(BLOG_DIR, map[TPL_PREV_ID] + HTML)
            do_template({TPL_NEXT: next}, prev, prev)
        # save current file name so we can update next there next time
        write_single_line(map[TPL_ID], PREV_FILE)
        # generate main page
        do_template(map, INDEX, INDEX_FILE)
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


