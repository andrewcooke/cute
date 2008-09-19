#!/usr/bin/python2.5

from __future__ import with_statement

from email import message_from_file
from sys import stderr
from os import listdir
from os.path import isfile, getctime
from re import compile

from cute import add_new_entry, add_reply, Multipart, BadSubject, get_time
from constants import *


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
    collect_files('/home/andrew/mail/.play.lists.tech.compute/cur',
                  TYPE_ARTICLE, files)
    collect_files('/home/andrew/mail/.play.lists.tech.compute/new',
                  TYPE_ARTICLE, files)
    collect_files('/home/andrew/mail/.play.lists.tech.compute.reply/cur',
                  TYPE_REPLY, files)
    collect_files('/home/andrew/mail/.play.lists.tech.compute.reply/new',
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

if __name__ == '__main__':
    main()
