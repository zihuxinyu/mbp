# coding: utf-8
'''
description:
Created by weibaohui on 14-5-15.

'''

import redis
r = redis.StrictRedis(host='134.44.36.125', port=6379, db=0,password='%$s%dd$%d#s^df#$a^fd%sf*^&(d*d&^)gh*^jk*e(*&e*s#%')
r.set('foo', 'bar')

s=r.get('foo')
print(s)