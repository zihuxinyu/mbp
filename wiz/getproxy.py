#! /usr/bin/python
# -*- coding: utf8 -*-
import sys
import threading

import os

sys.path.append(os.getcwd() + "\\Library")
import requests
import random
import time
from random import choice

import linecache
from Library import LogHelper
import re


class ProxyChecker:
    "代理服务器检测类，内部使用多线程方式用来检测指定的代理服务器列表中的代理服务器是否可用"

    def __init__(self, proxies, threadNum):
        self.proxies = proxies
        self.threadNum = threadNum

        self.mutex = threading.Lock()

    def execute(self):

        threads = []
        proxiesLen = max(len(self.proxies), self.threadNum)
        # 这里除以threadNum(比如等于20)是想用20个线程去跑，需要计算出范围切断，比如100个代理服务器分20段则每段5个
        space = proxiesLen / self.threadNum
        for num in range(self.threadNum):
            beginIndex = space * num
            endIndex = min(space * (1 + num), proxiesLen)
            t = ProxyCheckerThread("线程" + str(num + 1), self.proxies[beginIndex:endIndex],

                                   self.mutex)
            t.start()
            threads.append(t)


class ProxyCheckerThread(threading.Thread):
    "代理服务器检测器线程，检测代理服务器列表中的代理服务器是否能可用"

    def __init__(self, threadName, proxies, mutex):
        threading.Thread.__init__(self, name=threadName)
        self.proxies = proxies
        self.mutex = mutex

    def run(self):

        for proxyitem in self.proxies:
            try:

                _proxies = {"http": "http://" + proxyitem}
                r = requests.get('http://www.baidu.com', proxies=_proxies, timeout=1)
                if r.status_code == 200:

                    if self.mutex.acquire(1):
                        fileop = open(os.getcwd() + "/ip.txt", 'a+')
                        fileop.write(proxyitem + '\n')
                        fileop.close()

                        self.mutex.release()
                else:
                    continue
            except Exception, e:
                #print "use %s:%s to open baidu occured problem:%s" % (ip, port, e)
                continue


headers = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}


def getPageList(url, file):
    """
    获取关联的代理页面
    :param url:
    :param file:
    """
    f = requests.get(url + file, headers=headers)
    html = f.content
    html = html.decode('gbk', 'ignore')
    #print(html)
    page_rule = re.compile(r"<li><a href='(.+?)'[^\>]*>.+?</a></li>")
    for m in page_rule.finditer(html):
        if '_' in m.group(1):
            print(m.group(1))
            getProxy(url, m.group(1))


def getProxy(url, file):
    """
    获取页面内的IP地址
    :param url:
    :param file:
    """
    f = requests.get(url + file, headers=headers)
    html = f.content
    html = html.decode('gbk', 'ignore')
    #print(html)



    Serch_rule = re.compile(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}:.*@\b")
    proxies = []
    for m in Serch_rule.finditer(html):
        ip = m.group().replace('@', '')
        proxies.append(ip)

    threadNum = 50  #开50个线程去分工处理检测代理服务器
    s = ProxyChecker(proxies, threadNum)
    s.execute()

    #print(file, 'end')


if __name__ == '__main__':
    #os.remove(os.getcwd() + "/ip.txt")
    getPageList('http://www.youdaili.cn/Daili/guonei/', '1768.html')
