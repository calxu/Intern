#!/usr/bin/env python
#encoding:utf-8
"""
Spider: Collect data from http://zhixing.court.gov.cn/search/
Authors: Calvin,Xu
"""

import urllib2
import time
import socket
import random
import threading
import Captcha
import sys
import re
import datetime

reload(sys)
sys.setdefaultencoding('utf-8')

class MyThread(threading.Thread):
    """ 
        This class provides the API for the crawler. You can call the API through 
        MyThread(threadId, beginId, iterLength, proxy). In spider.py file, the call
        appear in 54 line.
    """

    def __init__(self, threadId, beginId, iterLength, proxy):
        """ Initialize parameter value. """
        threading.Thread.__init__(self)            # Call the parent function constructor

        self.name = threading.current_thread().name    # assign thread name
        """
        The threadId, beginId and iterLength determine the range of the thread. The range
        of the thread is [beginId+threadId*iterLength, beginId+(threadId+1)*iterLength-1].
        In spider.py file, the range appears in 56 line.
        """ 
        self.threadId = threadId
        self.beginId = beginId  
        self.iterLength = iterLength
        self.proxyMeta = proxy            # If you use proxy, please assign the proxy
        self.moment = datetime.datetime.now()
        self.captchaList = '0123456789abcdefghijklmnopqrstuvwxyz'

    def writeDistributedFile(self, data):
        """ Write data to the distributedFile. """
        fileAddress = '../distributedFile/' + str(self.threadId) 
        with open(fileAddress, 'a') as f:
            f.write(data + '\n')

    def getCaptcha(self, data):
        """ Get the captcha value through calling Capthca.py. """
        fileAddress = '../temporaryPicture/' + str(self.threadId) + ".jpg"
        with open(fileAddress, 'wb') as f:                       # the picture is binary file.
            f.write(data)
        return Captcha.getCaptcha(str(self.threadId))            # achieve the captcha value
            
    def getBinary(self, strUrl, flag=False):
        """ 
           The function is to crawl binary web page. The flag variable tag is mark whether to capture the 
           captcha or web page json content. If flag is false, it represent it is picture crawler request 
           and it do not have timeout. Otherwise, it represent it is web json content crawler request and 
           it should consider timeout.
        """
        name = self.name                                         # threading name
        
        # proxy server
        # proxy = urllib2.ProxyHandler({'http':self.proxyMeta, 'https':self.proxyMeta})
        # opener = urllib2.build_opener(proxy)
        # urllib2.install_opener(opener)
        # the brower header
        my_header = {
                     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0',
                     'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                     'Accept-Encoding':'Accept-Encoding:gzip, deflate, sdch',
                     'Accept-Language':'zh-CN,zh;q=0.8',
                     'Cache-Control':'max-age=0',
                     'Connection':'keep-alive',
                     'Cookie':'CNZZDATA4793016=cnzz_eid%3D668395505-1438110802-%26ntime%3D1438110802',
                     'If-None-Match':"95be97e83edad6c9f9c8dfbe47decc26",
                     'Upgrade-Insecure-Requests':'1',
                     'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.107 Safari/537.36'
                    }
        timeout = 10
        while True:
            try:
                if (flag == True) and \
                        (datetime.datetime.now()-self.moment).total_seconds() >= 180:  # web json content
                    data_binary = '{}'
                    break
                req = urllib2.Request(strUrl, headers = my_header)       # request
                response = urllib2.urlopen(req, timeout = 240) 
                data_binary = response.read()                            # binary file
                response.close()                                         # close the web
                break
            except urllib2.HTTPError as e:                               # some exception
                print name, 1, e
                time.sleep(random.choice(range(5, 20)))
            except urllib2.URLError as e:
                print name, 2, e
                time.sleep(random.choice(range(10, 100)))
            except socket.timeout as e:
                print name, 3, e
                timeout += random.choice(range(50, 200))
                time.sleep(timeout)
            except socket.error as e:
                print name, 4, e
                timeout += random.choice(range(50, 200))
                time.sleep(timeout)
            except Exception:
                print name, 5
                time.sleep(random.choice(range(10, 100)))
    
        return data_binary                                               # return binary file

    def getContent(self, strUrl, flag=False):
        """ download the json format. """
        try:
            html = self.getBinary(strUrl, flag).decode('UTF-8')          # decode the original file
        except:
            print self.name, self.getBinary(strUrl, flag)
            html = ''
        return html                                                      # return the html
    
    def WebReset(self, html):
        """ 
            Forbid web reset. Sometimes the pages are redirected to other pages.
            If the page is redirected, it returns true; otherwise it returns false.
        """
        if re.findall('<script type="text/javascript">', html) != []:
            print self.name, "请开启JavaScript并刷新该页 or 网站当前访问量较大请输入验证码后继续访问"
            time.sleep(random.randint(10, 80))           # wait for a while, and then visit the page.
            return True                                  # need to access again
        else:
            return False

    
    def getEffectiveCaptcha(self):
        """
            The accuracy of the tool tesseract is only about 8% approximately, so we should try to 
            get captcha repeatedly until getting correct captcha.
        """
        while True:
            # achieve the captchaId
            captchaId = ''
            i = 0
            while i <= random.randint(1, 50):
                captchaId += random.choice(self.captchaList)
                i += 1
            
            pictureURL = "http://zhixing.court.gov.cn/search/captcha.do?captchaId=" + captchaId
            data = self.getBinary(pictureURL)                      # achieve the picture
            
            # Forbid the web reset
            if self.WebReset(data):
                continue

            captcha = self.getCaptcha(data)                    # achieve the captcha value
            strURL = "http://zhixing.court.gov.cn/search/newdetail?id=2397486&j_captcha=" \
+ captcha + "&captchaId=" + captchaId
            html = self.getContent(strURL)          # only request once. Not need to consider timeout
            
            # Forbid the web reset
            if self.WebReset(html):                            # if get the java script, let continue
                continue       

            """ 
                The accuracy of open source tool tesseract is only about 8% approximately, so we need to 
                use a certain page information to ensure the correctness of the captcha. For example, in
                our situation, we use id 2,397,486 to identify correctness of the captcha. Theoretically,
                you will get {"id":2397486,"caseCode":"(2017)鲁1625执131号","caseState":"0","execCourtName"
                :"博兴县人民法院","execMoney":71550,"partyCardNum":"37232819791****121X","pname":"王峰",
                "caseCreateTime":"2017年01月23日"}. If you do not get it, the captcha you get is error.
            """
            if re.findall('{"id":2397486,"caseCode":.*}', html) != []:
                break                                          # the captcha will sustain 180 second

        print self.name, "successfully authentication"         # output into the log. Remind: the captcha will sustain 180 second
        return (captchaId, captcha)                            # return the captcha value corresponding to captchaid
    
    def run(self):
        """ Each thread crawl data. """
        count = 0; lastCount = 0
        flag = False                  # determine whether to get captcha again.
        iterLength = self.iterLength  # the number of iterations per thread

        while count < iterLength:
            # determine whether it is a new round of iteration
            if (count == 0) or (lastCount != count):
                beginTime = (datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
            lastCount = count                                  # the last count value
            
            # determine whether to get captcha again
            if flag or (count == 0):                          
                captchaId, captcha = self.getEffectiveCaptcha()# achieve effective captchaId and captcha
                self.moment = datetime.datetime.now()          # the start time of captcha valid
                flag = False                                   # determine whether to get captcha again
            
            while True:
                strURL = "http://zhixing.court.gov.cn/search/newdetail?id=" + str(self.beginId \
+ self.threadId * iterLength + count) + "&j_captcha=" + captcha + "&captchaId=" + captchaId 
                print self.name, strURL                        # URL address, output into log
                html = self.getContent(strURL, True)           # the captcha will sustain 180s, so you need to assign flag=True

                if (datetime.datetime.now()-self.moment).total_seconds() >= 180:
                    flag = True
                    count -= 1
                    html = '{}'
                    break
                
                if self.WebReset(html):                         # if get the java script, let continue
                    continue
                else:
                    break
                
            if re.findall('{"id":.*', html) != []:
                # write the json to the file
                endTime = (datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
                self.writeDistributedFile(beginTime + '\t' + endTime + '\t' + html[1:-1])
             
            if flag == False:                                      # success and then output into the log
                print self.name, self.beginId + self.threadId * iterLength + count, \
                        "(", (datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S"), ")"
            count += 1
