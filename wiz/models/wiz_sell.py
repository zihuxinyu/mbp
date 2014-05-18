# coding: utf-8
'''
description:
Created by weibaohui on 14-5-16.

'''
from pony.orm import *
from wiz.Logic.Mysqldb import db
from datetime import datetime


class wiz_sell(db.Entity):
    '''
    已售
    '''
    guid = PrimaryKey(int, auto=True)
    invite_code = Optional(unicode)
    price = Optional(int)
    realcount = Optional(int)
    reguser = Optional(unicode)
    regpsw = Optional(unicode)
    opdate = Optional(datetime, default=datetime.now())
