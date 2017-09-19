#!/usr/bin/env python
# encoding:utf8
"""
Handle search data during one day.
Authors: Calvin,Xu
"""
import sys


def readTable():
    """ Read the streaming data. """
    for line in sys.stdin:
        record = line.rstrip()
        print record


if __name__ == '__main__':
    readTable()
