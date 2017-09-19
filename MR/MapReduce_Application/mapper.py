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
        record = line.rstrip().split('\x01')
        print "\t".join([record[0], record[1], record[2]])


if __name__ == '__main__':
    readTable()
