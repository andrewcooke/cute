#!/usr/bin/python

from email import message_from_file
from sys import stdin
from subprocess import call

from cute import add_new_entry


def main():
    email = message_from_file(stdin)
    add_new_entry(email)
#    do_call('/home/andrew/bin/updateCute')
#    do_call('/home/andrew/bin/tweetCute')

def do_call(*args):
    print args
    call(args)

if __name__ == '__main__':
    main()
