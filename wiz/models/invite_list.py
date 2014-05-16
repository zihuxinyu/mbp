# coding: utf-8
'''
description:
Created by weibaohui on 14-5-16.

'''
from pony.orm import *
from wiz.Logic.Mysqldb import db
from datetime import datetime

class invite_list(db.Entity):
    '''
    邀请用户列表,为这些用户注册
    '''
    guid = PrimaryKey(int, auto=True)
    invite_code= Optional(unicode)
    type = Optional(unicode)
    askcount = Optional(int)
    realcount = Optional(int)
    opdate=Optional(datetime, default=datetime.now())
