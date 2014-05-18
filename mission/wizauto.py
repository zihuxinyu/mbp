# coding: utf-8
'''
description:
Created by weibaohui on 14-5-18.

'''
import  requests
import  time
if __name__=="__main__":
    url="http://dyit.org:8806/wiz/autostart/"
    while(True):
        r=requests.get(url)
        print(r.text)
        time.sleep(60*5)

    