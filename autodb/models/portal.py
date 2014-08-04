# coding: utf-8
'''
description:用户信息、角色信息、权限信息、模块信息
Created by weibaohui on 14-5-14.

'''
from autodb.Logic.Mysqldb import db
from pony.orm import *
from datetime import datetime


class users():
    user_code=None
    groupid=None
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
    id = PrimaryKey(int, auto=True)
    user_code = Optional(unicode)
    user_name = Optional(unicode)
    #user_mobile = Optional(unicode)
    dpt_name = Optional(unicode)
    topdpt = Optional(unicode)
    #manager = Optional(unicode)
    #msg = Optional(unicode)
    #msgexpdate = Optional(datetime,default=datetime.now())

class modulelist(db.Entity):
    '''
    模块列表，包含访问url信息,模块描述信息
    '''
    guid=PrimaryKey(int,auto=True)
    url=Optional(LongUnicode)
    modulename=Optional(unicode)
    doc= Optional(unicode)
    state=Optional(unicode,default='ok')
    modifierid=Optional(unicode)
    modifydate=Optional(datetime,default=datetime.now())
    creatorid=Optional(unicode)
    createdate=Optional(datetime, default=datetime.now())


class group_module(db.Entity):
    '''
    用户角色、模块对应关系表
    '''
    guid = PrimaryKey(int, auto=True)
    groupid = Required(int)
    modulename = Required(unicode)
    modifierid = Optional(unicode)
    modifydate = Optional(datetime, default=datetime.now())
    creatorid = Optional(unicode)
    createdate = Optional(datetime, default=datetime.now())


class menutree(db.Entity):
    '''
    菜单与模块、权限关系
    '''
    id = PrimaryKey(int, auto=True)
    pid = Optional(int,default=0)
    modulename = Optional(unicode)
    url = Optional(unicode)
    text = Optional(unicode)
    num=Optional(int,default=0)
    # modifierid = Optional(unicode)
    # modifydate = Optional(datetime, default=datetime.now())
    # creatorid = Optional(unicode)
    # createdate = Optional(datetime, default=datetime.now())
