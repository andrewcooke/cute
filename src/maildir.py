#!/usr/bin/python2.5

from email import message_from_file
from sys import stdin
from os import listdir
from os.path import isfile

from cute import add_new_entry


def main():
    for path in listdir('.'):
        if isfile(path) and not path.endswith('~'):
            with open(path) as source:
                email = message_from_file(source)
                add_new_entry(email)

if __name__ == '__main__':
    main()
