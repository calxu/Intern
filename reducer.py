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
    data = read_data( sys.stdin )
    
    for key, it in groupby(data, itemgetter(0)):
        # passid	value_id	confidence	table_mark
        table2_index = []                          # table2 index
        
        table1 = []
        for line in it:
            if (line[3] == "table2"):
                if int(line[2]) >= 90:
                    table2_index.append( line[1] )
            else:
                table1.append( line[1] )

        table2_index = list( set(table2_index) )   # remove the duplication
        
        value_id_list = []                         # passid list
        for line in table1:
            if line in table2_index: 
                value_id_list.append( line ) 
        
        if value_id_list != []:
            print '\t'.join( [ key, str(len( set(value_id_list) )) ] )


if __name__ == '__main__':
    main()
