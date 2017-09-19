#!/usr/bin/env python
#encoding:utf-8
"""
Spider API: python spider.py BeginId, EndId, threadNumbers
Authors: Calvin,Xu
"""

import sys
import os
import time
import random
from Collection import MyThread

def main(argv):
    """ 
        Main function, parameter: beginId, endId, threadNumbers. 
        For example, you can call the function through following code: python spider.py 13409155 14000000 1
        Traverse id from 1340,9155 to 1400,0000 through 1 thread. In this case, I assign the only one thread, you
        can assign multi-threads, but the web can identify crawler. So you need proxy agent to disguise yourself.
    """

    # Check the input parameter validity.
    while True:
        beginId = int(argv[1])
        endId   = int(argv[2])
        threadNumbers = int(argv[3])
        iterLength = (endId - beginId) / threadNumbers          # the iter times of each thread
        if iterLength * threadNumbers == (endId - beginId):     # judge whether int type or not
            break
        else:                                                   # prompt
            print "Please input appropriate beginId, endId and threadNumbers \
to make the (endId - beginId)/threadNumbers int type"
            return 
    
    # Create directory through shell command
    os.system("mkdir -p ../temporaryPicture")                     # save captcha picture
    os.system("mkdir -p ../distributedFile")                      # save the final data through distributed files
    
    """
      You can assigne relative proxy before you execute the program. You can achieve 
      proxys from https://www.abuyun.com/, but the proxys providers need charges. You
      can also capture data without assigning agents, but sometimes your crawler can be 
      recognized and can be interrupted. 
      
      abuyun platform proxy: proxy = "http://HE4531GH1974I50D:F7D02ACD78C46E36@proxy.abuyun.com:9020"
    """
    proxy = ""                                              # default: not use proxy
    threadId = 0
    threadList = []

    # initialize every thread
    while threadId < threadNumbers:
        t = MyThread(threadId, beginId, iterLength, proxy)
        t.name = "%04d\t%08d~%08d:"% \
            (threadId, beginId + threadId * iterLength, beginId + (threadId + 1) * iterLength - 1)
        threadList.append(t)
        threadId += 1


    print "主进程开始."

    # start thread
    threadId = 0
    while threadId < threadNumbers:
        threadList[threadId].start()
        time.sleep(2)
        threadId += 1

    threadId = 0
    while threadId < threadNumbers:
        threadList[threadId].join()
        threadId += 1

    # print "主进程结束"

    os.system("rm -rf ../temporaryPicture")                   # remove the temporary picture file

    # print "%08d~%08d successfully! please continue from %08d next week." % \
    #     (beginId, beginId + threadNumbers * iterLength - 1, beginId + threadNumbers * iterLength)


if __name__ == '__main__':
    main(sys.argv)
