# coding: utf-8
'''
description:
Created by weibaohui on 14-5-16.

'''
from pony.orm import *
from wiz.Logic.Mysqldb import db
from datetime import datetime


class proxy_list(db.Entity):
    '''
    代理列表
    '''
    guid = PrimaryKey(int, auto=True)
    proxy= Optional(unicode)

    opdate=Optional(datetime, default=datetime.now())
    