#!/usr/bin/env python
# encoding:utf8
"""
Handle search data during one day.
Authors: Calvin,Xu
"""
import sys
import os
import random
import re

def handle():
    """ Read the streaming data. """

    dataDict = dict()
    with open('xgb_featureIDMap', 'r') as f:
        data = f.readlines()
        for line in data:
            record = line.rstrip().split('\t')
            dataDict[record[0]] = record[1]

#     with open('featureScore', 'r') as f:
#         data = f.readlines()[0].rstrip()
#         scoreDict = eval(data)
        
    pattern = re.compile('\[f(.*)<')
    for line in sys.stdin:
        dataID = pattern.findall(line)
        if dataID != []:
            # print "f"+dataID[0], dataDict[dataID[0]] # , scoreDict['f'+dataID[0]]
            print line.rstrip().replace(dataID[0], dataDict[dataID[0]])
        else:
            print line.rstrip()


if __name__ == '__main__':
    handle()
