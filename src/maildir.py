#!/usr/bin/python

from email import message_from_binary_file
from logging import getLogger
from os import listdir
from os.path import isfile
from sys import stderr

from constants import *
from cute import add_new_entry, add_reply, Multipart, BadSubject, get_time, BadTime

log = getLogger(__name__)


def collect_files(dir, type_, acc):
    for file in listdir(dir):
        path = join(dir, file)
        if isfile(path) and not path.endswith('~'):
            try:
                time = get_time(path)
                acc.append((type_, time, path))
            except BadTime as e:
                log.warning(e)


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
    files.sort(key=lambda type_time_path: type_time_path[1])
    for (type_, time, path) in files:
        stderr.write('processing %s %s\n' % (path, type_))
        with open(path, 'rb') as source:
            try:
                email = message_from_binary_file(source)
                if type_ == TYPE_ARTICLE:
                    add_new_entry(email)
                else:
                    add_reply(email)
            except Multipart as e:
                log.warning(e)
            except BadSubject as e:
                log.warning(e)


if __name__ == '__main__':
    main()
