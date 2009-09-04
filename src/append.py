#!/usr/bin/python

from email import message_from_file
from sys import stdin
from subprocess import call

from cute import add_new_entry


def main():
    email = message_from_file(stdin)
    add_new_entry(email)
    call(['/home/andrew/bin/updateCute'])
    call(['/home/andrew/bin/tweetCute'])
    call(['/home/andrew/bin/rssping', 'rpc.technorati.com', '/rpc/ping'])
    call(['/home/andrew/bin/rssping', 'rpc.weblogs.com', '/RPC2'])
    call(['/home/andrew/bin/rssping', 'blogsearch.google.com', '/ping/RPC2'])

if __name__ == '__main__':
    main()
