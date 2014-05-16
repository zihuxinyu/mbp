# coding: utf-8
'''
description:
Created by weibaohui on 14-5-16.

'''

from pony.orm import *
from wiz.Logic.Mysqldb import db


class xiaomi(db.Entity):
    '''
    小米论坛泄露用户
    '''
    id = PrimaryKey(int, auto=True)
    username = Optional(unicode, default='')
    email = Optional(unicode, default='')
