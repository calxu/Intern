#!/usr/bin/env python
# encoding:utf8
import sys
import httplib
import os
import json
import socket
from multiprocessing import Pool


def http_post_httplib(id, captcha, captchaid):
    """
    获取网络请求
    :param passid: 要查询的key
    :return:数据,http状态码,命令行返回值
    """

    para = "id=" + str(id) + "&j_captcha=" + str(captcha) + "&captchaId=" + str(captchaid)
    headers = {"Content-Type": "application/json", "Accept": "text/plain"}
    conn = httplib.HTTPConnection("zhixing.court.gov.cn", 80, True, 3)
    try:
        conn.request("GET", "/search/newdetail?" + para)
        response = conn.getresponse()
        data = response.read()
        if (response.status == 200):
            print "\t".join([str(id), data])
            return data
        else:
            sys.stderr.write("resp code:" + str(response.status) + ", resp resean:" + response.reason + "\n")
            return response.reason
    except Exception as e:
        sys.stderr.writelines(response.reason)
        return response.reason
    finally:
        if conn:
            conn.close()
    return response.reason


if __name__ == '__main__':
    # 初始化参数
    pool = Pool(4)
    try:
        pool.apply(http_post_httplib,
            args=("11780432", "kbgd", "1900e891cf3a449b9b78f68b863e6e27",))
    except Exception as e:
        pool.close()
        pool.join()
