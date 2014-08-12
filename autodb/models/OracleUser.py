# coding: utf-8
'''
description:
Created by weibaohui on 14-6-8.
此为Oracle 数据库中信息，只读
'''
import uuid
from autodb.Logic.Oracledb import db
from pony.orm import *
from datetime import datetime
class EXT_DPT_USR(db.Entity):
    user_code = PrimaryKey(unicode)
    user_name = Required(unicode)
    user_mobile = Optional(unicode)
    dpt_name = Optional(unicode)
    topdpt = Optional(unicode)
    manager = Optional(unicode)
    rybh = Optional(unicode)


class EXT_USER_GROUP(db.Entity):
    """
    Oracle用户与角色对应关系表
    """
    guid=PrimaryKey(unicode)
    user_code=Required(unicode)
    user_name = Required(unicode)
    groupid=Required(unicode)
class EXT_GROUPLIST(db.Entity):
    '''
    角色信息
    '''
    guid = PrimaryKey(unicode)
    groupname= Required(unicode)#角色名称
    id= Required(unicode)#角色ID
    creatorid=Required(unicode)#创建者4A
