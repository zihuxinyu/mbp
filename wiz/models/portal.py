# coding: utf-8
'''
description:云门户用户
Created by weibaohui on 14-5-14.

'''
from wiz.Logic.Mysqldb import db
from pony.orm import PrimaryKey, Optional
from datetime import datetime


class users():
    user_code=None;
    def __init__(self,user_code):
        self.user_code=user_code

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.user_code)



class portal_user(db.Entity):
    guid = PrimaryKey(int, auto=True)
    user_code = Optional(unicode)
    user_name = Optional(unicode)
    user_mobile = Optional(unicode)
    dpt_name = Optional(unicode)
    topdpt = Optional(unicode)
    manager = Optional(unicode)
    msg = Optional(unicode)
    msgexpdate = Optional(datetime,default=datetime.now())


