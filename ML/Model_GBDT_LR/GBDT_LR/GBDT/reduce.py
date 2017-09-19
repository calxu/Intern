#!/usr/bin/python

import sys
import re

def main():
    """ Main function. """
    for line in sys.stdin:
        record = line.rstrip().split("\t")
        print "%s,%s" % (record[0], record[1])


if __name__ == "__main__":
    main()
