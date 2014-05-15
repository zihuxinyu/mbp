# coding: utf-8
'''
description:产生Mysql pony db
Created by weibaohui on 14-5-14.

'''
from autodb import cache
from Library.minihelper import getGridData
from pony.orm import *
from  autodb.config import DB_DATEBASE,DB_HOST,DB_PSW,DB_USER
db = Database('mysql', host=DB_HOST, user=DB_USER, passwd=DB_PSW, db=DB_DATEBASE)

@cache.memoize(60)
def getData(entity, total=999, data=None):
    return getGridData(entity,total,data)




