#!/usr/bin/env python
# coding:UTF-8

from sklearn import preprocessing
from math import exp
from numpy import *
import sys


def getParameter():
    indexDict = dict()                     # index dictionary
    v_parameter = zeros((99998, 5))
    w_parameter = zeros((99998, 1))
    with open('./featureIDMap', 'r') as f:
        for line in f.readlines():
            record = line.rstrip().split(' ')
            indexDict[record[1]] = int(record[0])   # store data

    with open('./w_v_vector', 'r') as f:
        for line in f.readlines():
            record = line.rstrip().split('\t')
            index = indexDict[record[0]]            # get the index
            row = record[1].split(' ')              # get the value
            w_parameter[index] = float(row[0])
            v_parameter[index][0] = float(row[2])
            v_parameter[index][1] = float(row[3])
            v_parameter[index][2] = float(row[4])
            v_parameter[index][3] = float(row[5])
            v_parameter[index][4] = float(row[6])
        
    return (w_parameter, v_parameter)


def getData():
    for line in sys.stdin:
        yield line.strip().split('\t')


def sigmoid(inx):
    return 1.0 / (1 + exp(-inx))


def getAccuracy(w, v):
    count = 0
    for row in getData():
        data = zeros((1, 99998))
        userID = row[0]
        dataDict = eval(row[1])
        for key in dataDict.keys():
            data[0][key] = float(dataDict[key])

        inter_1 = dot(data, v)
        inter_2 = dot(data * data, v * v)       # 对应元素相乘
        # 完成交叉项
        interaction = sum(inter_1 * inter_1 - inter_2) / 2.
        p = dot(data, w) + interaction  # 计算预测的输出
        
        print "dot(data, w)=", dot(data, w)
        print "interaction=", interaction
        print "dot(data, w)+interaction=", dot(data, w)+interaction
        print "p[0, 0]=", p[0, 0]
        value = sigmoid(p[0, 0])
        
        # print "%s\t%s" % (userID, value)


if __name__ == '__main__':
    
    # w, v = getParameter()
    # getAccuracy(w, v)
