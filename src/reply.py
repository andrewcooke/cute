#!/usr/bin/python

from email import message_from_file
from sys import stdin
from subprocess import call

from cute import add_reply


def main():
    email = message_from_file(stdin)
    add_reply(email)
    call('/home/andrew/bin/updateCute')

if __name__ == '__main__':
    main()
