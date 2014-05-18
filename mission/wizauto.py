# coding: utf-8
'''
description:
Created by weibaohui on 14-5-18.

'''
import  requests
import  time
from datetime import datetime
if __name__=="__main__":
    url="http://dyit.org:8806/wiz/autostart/"
    while(True):
        if (datetime.now().time().hour>6 and datetime.now().time().hour <23):
            #r=requests.get(url)
            #print(r.text)
            pass
        time.sleep(60*60)

    