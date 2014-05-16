# coding: utf-8
'''
description:
Created by weibaohui on 14-5-16.

'''
from pony.orm import *
from wiz.Logic.Mysqldb import db
from datetime import datetime


class wiz_user(db.Entity):
    '''
    注册用户列表
    '''
    guid = PrimaryKey(int, auto=True)
    invite_code= Optional(unicode)
    proxy = Optional(unicode)
    reguser = Optional(unicode)
    regcode = Optional(unicode)
    regpsw = Optional(unicode)
    opdate=Optional(datetime, default=datetime.now())
    