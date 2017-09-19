#!/usr/bin/python

import sys
import re

def decodeLeaves():
    """ Map leaves to one hot. """
    boosterPattern = re.compile("booster\[(\d*?)\]")          # new booster pattern
    leafPattern = re.compile("(\d*?):leaf=")                  # leaves pattern
    
    leavesToIndex = dict()           # leaves to index

    with open("model_dump", "r") as f:
        modelDump = f.readlines()                             # model dump file
        modelDump.append("EOF")                               # add the terminator
        Leaves = dict()                                       # leaves dictionary
        leavesNum = 0                                         # leaves index
        boosterKey = 0                                        # booster times
        for line in modelDump[1:]:
            treeLeaf = re.findall(leafPattern, line)          # the leaf of the tree
            if treeLeaf != []:                                
                Leaves[int(treeLeaf[0])] = leavesNum          # the leaf index of the current tree 
                leavesNum += 1
            
            boosterId = re.findall(boosterPattern, line)      # judge whether new booster iteration
            if boosterId != []:
                boosterKey = int(boosterId[0])                # dict key
                leavesToIndex[boosterKey-1] = Leaves
                Leaves = dict()
            elif line == "EOF":
                    leavesToIndex[boosterKey] = Leaves
    
        leavesToIndex["sum"] = leavesNum                      # the list of leaves to index
    
    return leavesToIndex 


def convert(leavesToIndex):
    """ Handle output of gbdt. """
    for line in sys.stdin:
        record = line.rstrip().split(',')
        output = record[0] + "\t" + record[1] + ","           # user label
        
        boosterIndex = 0                                      # booster index
        for leavesIndex in record[3:]:
            output += str(leavesToIndex[boosterIndex][int(leavesIndex)]) + ","
            boosterIndex += 1
        
        print output[:-1]


def main():
    """ Main function. """
    leavesToIndex = decodeLeaves()
    convert(leavesToIndex)


if __name__ == "__main__":
    main()
