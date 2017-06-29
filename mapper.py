#!/usr/bin/env python
# encoding:utf8
import sys
import re


def device_filter(device_type, device_id):
    """ 格式化设备id,不规范的设备id置为空""" 
    # preprocess cuid
    if device_type == '3':
        device_id = device_id.replace('%7C', '|')
        if ( len(device_id) not in [32, 40, 48, 51] or 
                re.match(r'([\w]{32}\|[\w]{15})|([\w]{32})|([\w]{40})|([\w]{51})', device_id) is None ):
            device_id = ''
    # preprocess imei
    elif device_type == '4':
        device_id = device_id if device_id.strip('0') != '' else ''
        if (len(device_id) not in [14, 15, 16]) or (re.match(r'[\w]{14,16}', device_id) is None):
            device_id = ''

    return device_id


def readTable():
    """ Read the table """
    for line in sys.stdin:
        yield line.rstrip().split('\t')


def main(device_type='4'):
    """ main """
    table = readTable()
    
    index = 1                          # imei下标
    if device_type == '4':
        index = 1
    elif device_type == '3':
        index = 2

    for line in table:
        if len(line) == 3:
            if device_filter(device_type, line[index]) == '':
                continue
            print '\t'.join( [line[0], line[index], 'line[4]', 'table1'] )    # passid value_id 'line[4]'  table1
        elif len(line) == 5:
            if line[1] == device_type:
                if device_filter(device_type, line[2]) == '':
                    continue
                print '\t'.join( [line[0], line[2], line[4], 'table2'] )      # passid value_id confidence  table2
 

if __name__ == '__main__':
    main('4')             # imei or cuid
