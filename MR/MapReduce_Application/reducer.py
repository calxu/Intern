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
    """main."""
    data = readInput(sys.stdin)
    
    for key, it in groupby(data, itemgetter(0)):
        # userid    search content  date
        searchTerms = set()
        date = ""
        
        for record in it:
            if len(record) == 3:
                date = record[2]

            try:
                searchTerms.add(record[1].strip())
            except:
                continue
        
        if (len(searchTerms) == 0) or (date == ""):      # If empty, then continue
            continue

        searchTerms = "\x01".join(searchTerms)
        
        print "\t".join([key, searchTerms, date])


if __name__ == "__main__":
    main()
