__author__ = 'weibaohui'
# coding: utf-8
# encoding: UTF-8

import urllib2, re, threading, time


class ProxyFinderThread(threading.Thread):
    "解析查找指定url的代理服务器信息线程"

    def __init__(self, threadName, url, parser, resultLst, mutex):
        threading.Thread.__init__(self, name=threadName)
        self.url = url
        self.parser = parser
        self.resultLst = resultLst
        self.mutex = mutex

    def run(self):
        html = getHtml(self.url)
        proxies = self.parser(html)
        if self.mutex.acquire(1):
            self.resultLst.extend(proxies)
            print self.name + "查找" + str(self.url) + "中的代理服务器信息，并将查找结果追加进结果列表：" + str(self.resultLst)
            self.mutex.release()


class ProxyFinder:
    "代理服务器查找类，内部使用多线程去查找指定url的代理服务器信息"

    def __init__(self):
        self.resultLst = []
        self.mutex = threading.Lock()
        self.urlParserMap = {}

    def put(self, url, parser):
        self.urlParserMap[url] = parser

    def findProxies(self):
        threads = []
        for index, url in enumerate(self.urlParserMap.keys()):
            parser = self.urlParserMap[url]
            t = ProxyFinderThread("线程" + str(index + 1), url, parser, self.resultLst, self.mutex)
            t.start()
            threads.append(t)

        print "\n\n主(main)线程在使用join方法来等待所有查找代理服务器线程执行完毕..."
        for t in threads:
            t.join()
        print "\n所有查找代理服务器线程已经执行完毕!查找到的所有代理服务器结果列表为：\n" + str(self.resultLst)
        return self.resultLst


def getHtml(url):
    try:
        return urllib2.urlopen(url).read()
    except:
        print "can not open the url:" + url
        return ""


def findProxies(html):
    "抓取http://www.proxy360.cn/Proxy代理服务器信息的解析器"

    pStr = r'''<span class="tbBottomLine" style="width:140px;">\s*(.+?)\s*</span>\s*<span class="tbBottomLine" style="width:50px;">\s*(.+?)\s*</span>'''
    p = re.compile(pStr)
    r = p.findall(html)
    return r


def findProxies2(html):
    "抓取www.cnproxy.com/proxy1.html代理服务器信息的解析器"

    table = {'z': '3', 'm': '4', 'a': '2', 'l': '9', 'f': '0', 'b': '5', 'i': '7', 'w': '6', 'x': '8', 'c': '1'}
    pStr = r'''<tr><td>(.+?)<SCRIPT type=text/javascript>document\.write\(":"\+(.+?)\)</SCRIPT></td><td>.+?</td><td>.+?</td><td>.+?</td></tr>'''
    p = re.compile(pStr)
    pr = p.findall(html)
    result = []
    for ip, portStr in pr:
        try:
            result.append((ip, "".join(map(lambda x: table[x], portStr.split("+")))))
        except KeyError:
            print ip + ":" + portStr + "\n"
    return result


class ProxyCheckerThread(threading.Thread):
    "代理服务器检测器线程，检测代理服务器列表中的代理服务器是否能可用"

    def __init__(self, threadName, proxies, resultLst, mutex):
        threading.Thread.__init__(self, name=threadName)
        self.proxies = proxies
        self.resultLst = resultLst
        self.mutex = mutex

    def run(self):
        cookies = urllib2.HTTPCookieProcessor()
        for ip, port in self.proxies:
            self.__installProxyOpener__(cookies, ip, port)
            try:
                currentTime = time.time()
                req = urllib2.urlopen("http://www.baidu.com", timeout=5)
                elapse = time.time() - currentTime
                html = req.read()
                if html.rfind("030173") != -1:
                    if self.mutex.acquire(1):
                        self.resultLst.append((ip, port, elapse))
                        print self.name + "检测" + str(ip) + ":" + str(port) + "代理服务器成功，并将该代理服务器追加进结果列表：" + str(
                            self.resultLst)
                        self.mutex.release()
                else:
                    continue
            except Exception, e:
                #print "use %s:%s to open baidu occured problem:%s" % (ip, port, e)
                continue

    def __installProxyOpener__(self, cookies, ip, port):
        proxy_handler = urllib2.ProxyHandler({"http": r'http://%s:%s' % (ip, port)})
        opener = urllib2.build_opener(cookies, proxy_handler)
        opener.addheaders = [('User-agent', 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322)')]
        urllib2.install_opener(opener)


def my_cmp(x, y):
    "自定义的排序规则，因为排序对象是元组，需要用元组第3个值（代理服务器访问百度页面时间）来排序"
    return cmp(x[2], y[2])


class ProxyChecker:
    "代理服务器检测类，内部使用多线程方式用来检测指定的代理服务器列表中的代理服务器是否可用"

    def __init__(self, proxies, threadNum):
        self.proxies = proxies
        self.threadNum = threadNum
        self.resultLst = []
        self.mutex = threading.Lock()

    def execute(self):
        threads = []
        proxiesLen = max(len(self.proxies), self.threadNum)
        # 这里除以threadNum(比如等于20)是想用20个线程去跑，需要计算出范围切断，比如100个代理服务器分20段则每段5个
        space = proxiesLen / self.threadNum
        for num in range(self.threadNum):
            beginIndex = space * num
            endIndex = min(space * (1 + num), proxiesLen)
            t = ProxyCheckerThread("线程" + str(num + 1), proxies[beginIndex:endIndex], self.resultLst, self.mutex)
            t.start()
            threads.append(t)

        print "\n\n主(main)线程在使用join方法来等待所有代理服务器检测器线程执行完毕..."
        for t in threads:
            t.join()
        self.sort()
        result = self.resultLstStr()
        print "\n所有代理服务器检测器线程已经执行完毕!成功检测的所有代理服务器结果列表为：\n" + result
        self.save(result)

    def sort(self):
        self.resultLst.sort(my_cmp)
        #self.resultLst = sorted(self.resultLst, cmp=lambda x,y:cmp(x[2], y[2]))

    def resultLstStr(self):
        return "\n".join(map(lambda x: str(x), self.resultLst))

    def save(self, result):
        f = open(r'C:\proxy\proxy.txt', 'w')
        f.write(result)
        f.close()


if __name__ == "__main__":
    proxyFinder = ProxyFinder()
    proxyFinder.put("http://www.proxy360.cn/Proxy", findProxies)
    proxyFinder.put("http://www.cnproxy.com/proxy1.html", findProxies2)
    #有多个url且也实现了相应的解析器的话可以继续添加，例如
    #proxyFinder.put("http://www.cnproxy.com/proxy2.html", findProxies2)
    #proxyFinder.put("http://www.cnproxy.com/proxy3.html", findProxies2)
    #proxyFinder.put("http://www.cnproxy.com/proxy4.html", findProxies2)
    proxies = proxyFinder.findProxies()
    threadNum = 50  #开50个线程去分工处理检测代理服务器
    ProxyChecker(proxies, threadNum).execute()