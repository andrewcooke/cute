#!/usr/bin/python

from __future__ import with_statement

from email import message_from_file
from os import listdir
from os.path import isfile
from sys import stderr

from constants import *
from cute import add_new_entry, add_reply, Multipart, BadSubject, get_time


def compare_age((typea, timea, patha), (typeb, timeb, pathb)):
    return cmp(timea, timeb)


def collect_files(dir, type_, acc):
    for file in listdir(dir):
        path = join(dir, file)
        if isfile(path) and not path.endswith('~'):
            time = get_time(path)
            acc.append((type_, time, path))


def main():
    files = []
    collect_files('/home/andrew/mail/.compute/cur',
                  TYPE_ARTICLE, files)
    collect_files('/home/andrew/mail/.compute/new',
                  TYPE_ARTICLE, files)
    collect_files('/home/andrew/mail/.compute.reply/cur',
                  TYPE_REPLY, files)
    collect_files('/home/andrew/mail/.compute.reply/new',
                  TYPE_REPLY, files)
    files.sort(compare_age)
    for (type_, time, path) in files:
        stderr.write('processing %s %s\n' % (path, type_))
        with open(path) as source:
            try:
                email = message_from_file(source)
                if type_ == TYPE_ARTICLE:
                    add_new_entry(email)
                else:
                    add_reply(email)
            except Multipart, e:
                stderr.write(e.message)
            except BadSubject, e:
                stderr.write(e.message)
#            except Exception, e:
#                stderr.write(e.message)


def test():
    for path in ['/home/andrew/foo']:
        with open(path) as source:
            email = message_from_file(source)
            add_new_entry(email)


if __name__ == '__main__':
    main()
    # test()
