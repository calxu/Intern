#!/usr/bin/env python
# encoding:utf8
"""
Handle search data during one day.
Authors: Calvin,Xu
"""
import sys
from operator import itemgetter
from itertools import groupby


def readInput(data):
    """ Read the input streaming data. """
    for line in data:
        yield line.rstrip().split('\t')


def main():
    """ main. """
    data = readInput(sys.stdin)
    
    for key, it in groupby(data, itemgetter(0)):
        # userid    search content  date
        date = "20170501"
        searchTerms = set()
        for record in it:
            try:
                if int(record[2]) > int(date):
                    date = record[2]
            except:
                print record
        continue
            
            searchTerms = searchTerms | set(record[1].split('\x01'))

        searchTerms = "\x01".join(searchTerms)
        
        print "\t".join([key, searchTerms, date])


if __name__ == "__main__":
    main()
