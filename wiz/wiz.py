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
import urllib2
import xmlrpclib


class Urllib2Transport(xmlrpclib.Transport):
    def __init__(self, opener=None, https=False, use_datetime=0):
        xmlrpclib.Transport.__init__(self, use_datetime)
        self.opener = opener or urllib2.build_opener()
        self.https = https

    def request(self, host, handler, request_body, verbose=0):
        proto = ('http', 'https')[bool(self.https)]
        req = urllib2.Request('%s://%s%s' % (proto, host, handler), request_body)
        req.add_header('User-agent', self.user_agent)
        self.verbose = verbose
        return self.parse_response(self.opener.open(req))


class HTTPProxyTransport(Urllib2Transport):
    def __init__(self, proxies, use_datetime=0):
        opener = urllib2.build_opener(urllib2.ProxyHandler(proxies))
        Urllib2Transport.__init__(self, opener, use_datetime)


def getproxies():
    count = len(open('ip.txt', 'rU').readlines())  #获取行数
    hellonum = random.randrange(1, count, 1)  #生成随机行数
    proxys = {"http": "http://" + open('ip.txt', 'rU').readlines()[hellonum].replace('\n', '')}
    return proxys


class DoerThread(threading.Thread):
    def __init__(self, threadName, user_id, invite_code, proxies, transport):
        threading.Thread.__init__(self, name=threadName)
        self.user_id = user_id
        self.invite_code = invite_code
        self.proxies = proxies
        self.transport = transport
        self.threadName= threadName

    def run(self):
        try:
            LogHelper.Debug(self.threadName)
            do(self.user_id, self.invite_code, self.proxies, self.transport)
        except Exception,e:
            LogHelper.Debug(self.threadName+e.message+"error")
            pass


def do(user_id, invite_code, proxies, transport):

    headers = {
        "Host": "note.wiz.cn",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.2; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0",
        "Accept": "*/*",
        "Accept-Language": "zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3",
        "Accept-Encoding": "gzip, deflate",
        "DNT": "1",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "http://note.wiz.cn/register",
        "Cookie": "iCode=" + invite_code + "; wizuser=",
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "X-Forwarded-For": '{0}.{1}.{2}.{3}'.format(random.randint(0, 255), random.randint(0, 255),
                                                    random.randint(0, 255),
                                                    random.randint(0, 255))
    }

    url = 'http://note.wiz.cn/api/register'
    values = {
        "invite_code": invite_code,
        "password": "123456",
        "user_id": user_id
    }
    r = requests.post(url, data=values, headers=headers, proxies=proxies)
    LogHelper.Debug(r.content.decode('utf8'))
    cookie_str = r.json()['cookie_str']


    pcloginurl = "http://as.wiz.cn/wizas/xmlrpc"


    server = xmlrpclib.ServerProxy(pcloginurl, transport=transport, encoding=None, verbose=False, allow_none=False,
                                   use_datetime=False)
    result = server.accounts.clientLogin({'api_version': '3',
                                          'client_type': 'WIN',
                                          'client_version': '4.1.17.1',
                                          'password': 'md5.e10adc3949ba59abbe56e057f20f883e',
                                          'program_type': 'normal',
                                          'protocol': 'http',
                                          'user_id': user_id
    })
    time.sleep(3)
    resultiphone = server.accounts.clientLogin({'api_version': '3',
                                                'client_type': 'IPHONE',
                                                'client_version': '4.3.1',
                                                'password': 'md5.e10adc3949ba59abbe56e057f20f883e',
                                                'program_type': 'normal',
                                                'protocol': 'http',
                                                'user_id': user_id
    })
    #print ("invite_code:", result['invite_code'])
    fileop = open(os.getcwd() + "/ok.txt", 'a+')
    fileop.write(proxies['http'] + 'user' + invite_code + ':reg' + user_id + ':123456:' + result['invite_code'] + '\n')
    fileop.close()
    LogHelper.Debug(proxies['http'] + 'user' + invite_code + ':reg' + user_id + ':123456:' + result['invite_code'])

#time.sleep(3)
if __name__ == "__main__":
    #invite_code='2d935864' #mumu
    #invite_code='e42ad138' #zihu
    #invite_code='e947165d' #weibaohui@yeah.net

    #invite_code = '33d03f14'  #xieyk1
    invite_code = '4b9f6b25'  #zhaocl
    #invite_code='49462f9f'
    i = 800

    try:
        os.remove(os.getcwd() + "/ok.txt")
    except:
        pass


    for x in range(int(i)):
        #LogHelper.Debug(x)
        realmail = (open('1.txt').readlines()[random.randint(0, 1048549)]).strip("\r\n")
        email = ['139.cn', 'sohu.com', 'gmail.com', 'hotmail.com', '189.cn', '163.com', 'qq.com', '126.com',
                 'yahoo.com', 'sina.com', '21cn.com', '51admin.com', 'baidu.com', 'live.com', '163.com', 'qq.com',
                 '126.com', 'yeah.net', 'wo.com.cn', '263.com', 'tom.com', '360.cn', '51.com', '5d6d.cn', 'ysy.edu.cn',
                 'agri.gov.cn', 'ahut.edu.cn', 'ccec.edu.cn', '163.com', 'qq.com', '126.com', 'aisino.com', 'alg.com',
                 'bnu.edu.cn', 'ccidnet.com', 'chinaren.com', 'xsyu.edu.cn', '163.com', 'qq.com', '126.com', '163.com',
                 'qq.com', '126.com']
        id = '{0}{1}@{2}'.format(realmail, random.randint(0, 9999), choice(email))
        proxies=getproxies()
        transport=HTTPProxyTransport(proxies)
        t = DoerThread('T' + str(x), id, invite_code=invite_code,proxies=proxies,transport=transport)
        t.start()
        time.sleep(1)
