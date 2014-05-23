# _*_ coding:utf8 _*_
import requests
import random
import time
import re
from random import choice


def do(ip):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Maxthon/4.1.0.1600 Chrome/26.0.1410.43 Safari/537.1",
        "X-Forwarded-For": ip,
        "Referer": "http://vote.dongyingnews.cn/module/vote/content/?id=15",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-Hans,en-US;q=0.7,en;q=0.3",
        "Accept-Encoding": "gzip, deflate",
        "Host": "vote.dongyingnews.cn",
        "DNT": "1",
        "Connection": "Keep-Alive",
        "Cache-Control": "no-cache",
        "Cookie": "PHPSESSID=ahqsjs8b75t91c2mgv5485s4u5"
    }


    pageurl='http://vote.dongyingnews.cn/module/vote/content/?id=15'
    r = requests.get(pageurl, headers=headers)
    reg= r"<input type='hidden' .*?value='(.*?)'.*?>"
    keys=re.findall(reg, r.text)[0]



    id = ['356', '319', '357', '337', '329', '328', '316', '315', '322', '318', '351', '332', '312', '314', '320',
          '352', '349', '338', '358', '343', '323', '313', '359', '360', '334', '336', '327', '344', '346', '310']


    theid=choice(id)
    theid=356
    url = 'http://vote.dongyingnews.cn/module/vote/content/?mode=&fied=&sort=&action=post&id=15'


    values="keys={0}&G-37%5B%5D={1}&G-37%5B%5D={2}&G-37%5B%5D={3}&G-37%5B%5D={4}&G-37%5B%5D={5}&G-37%5B%5D={6}&G-37" \
           "%5B%5D={7}&G-37%5B%5D={8}&G-37%5B%5D={9}&G-37%5B%5D={10}".format(keys,337, choice(id), choice(id),choice(id), choice(id),
                                                                             choice(id), choice(id), choice(id),
                                                                             choice(id), choice(id))
    r = requests.post(url, data=values, headers=headers)
    print( '谢谢您的参与' in  r.text)




if __name__ == "__main__":
    while 1:

        ip1 = [27, 39, 112, 119, 182, 124, 60, 113, 123, 122, 211, 218, 59, 222, 221, 150, 153, 219, 58, 106, 61, 180,
               114, 202, 103, 203]
        ip2 = [192, 64, 224, 176, 32, 128, 208, 120, 4, 232, 168, 164, 56, 80, 132, 174, 0, 138, 118, 214, 206, 86, 218,
           162, 216, 14, 74, 235, 2, 58, 173, 156, 201, 115, 121, 122, 179, 223, 133, 3, 98, 59, 110, 136, 102, 22, 93]
        ip = '{0}.{1}.{2}.{3}'.format(choice(ip1), choice(ip2), random.randint(0, 255), random.randint(0, 255))
        print(ip)
        do(ip)
        time.sleep(1)