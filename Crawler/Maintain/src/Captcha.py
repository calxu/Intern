#!/usr/bin/env python
#encoding:utf8
"""
Identify captcha program.
Authors: Calvin,Xu
"""

import os
 
def getCaptcha(filename):
    """ 
        Identify the capthcha, and return Captcha value. 
    """

    # call the opensource tools to identify the captcha
    shellCommand = 'tesseract' + ' ../temporaryPicture/' + filename + \
'.jpg ../temporaryPicture/' + filename + ' -l eng -psm 7 digits'
    # print shellCommand
    # execute shell command 
    os.system(shellCommand)

    outputName = '../temporaryPicture/' + filename + ".txt"       # output file(Captcha)
    # print outputName

    with open(outputName, 'r') as f:
        Captcha = f.readline().rstrip().replace(' ', '')         # read the captcha value
    
    # delete the captcha file and the captcha picture
    os.system('rm ' + outputName + ' ../temporaryPicture/' + filename + '.jpg')

    return Captcha                     # return the captcha value


# local test code.
if __name__ == '__main__':
    Captcha = getCaptcha("7")
    print Captcha
