#!/usr/bin/env python
# encoding:utf8
import sys
from operator import itemgetter
from itertools import groupby


def read_data(file):
    """ read the data. """
    for line in file:
        yield line.rstrip().split('\t')

def main():
    """ count the number """
    data = read_data(sys.stdin)
    for key, it in groupby(data, itemgetter(0)):
        print key

if __name__ == '__main__':
    main()
