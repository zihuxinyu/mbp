# coding: utf-8
'''
description:sqlresultModel
Created by weibaohui on 14-5-14.

'''
from autodb.Logic.Mysqldb import db
from pony.orm import *
from datetime import datetime


class sqllist(db.Entity):
    __tablename__ = 'sqllist'

    guid = PrimaryKey(int, auto=True)
    title = Optional(unicode)
    state = Optional(unicode)

    sqlcontent = Optional(LongUnicode)
    paras = Optional(unicode)
    frequency = Optional(unicode)
    lastexec = Optional(datetime)
    nextexec = Optional(datetime)
    user_code = Optional(unicode)
    opdate = Optional(datetime, default=datetime.now())
#    modifierid = Optional(unicode)
#    modifydate=Optional(datetime,default=datetime.now())

