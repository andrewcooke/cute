#!/usr/bin/python2.5

from email import message_from_file
from sys import stdin

from cute import add_new_entry


def main():
    email = message_from_file(stdin)
    add_new_entry(email)

if __name__ == '__main__':
    main()
