#!/usr/bin/python

from email import message_from_file
from sys import stdin
from os import execl

from cute import add_new_entry


def main():
    email = message_from_file(stdin)
    add_new_entry(email)
    execl('/home/andrew/bin/updateCute')
    execl('/home/andrew/bin/rssping', 'rpc.technorati.com', '/rpc/ping')
    execl('/home/andrew/bin/rssping', 'rpc.weblogs.com', '/RPC2')
    execl('/home/andrew/bin/rssping', 'blogsearch.google.com', '/ping/RPC2')
    execl('/home/andrew/bin/tweetCute')

if __name__ == '__main__':
    main()
