# coding: utf-8
'''
description:sqlresultModel
Created by weibaohui on 14-5-14.

'''
from Logic.Mysqldb import db
from pony.orm import *
from datetime import  datetime

class sqlresult(db.Entity):
    __tablename__ = 'sqlresult'
    guid = PrimaryKey(int,auto=True)
    sguid = Optional(unicode)
    sqlcontent = Optional(unicode)
    success = Optional(unicode)
    message = Optional(unicode)
    opdate=Optional(datetime,default=datetime.now())

db.generate_mapping()