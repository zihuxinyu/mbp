# coding: utf-8
'''
description:
Created by weibaohui on 14-6-8.

'''
from autodb.Logic.Oracledb import db
from pony.orm import *

class EXT_DPT_USR(db.Entity):
    user_code = PrimaryKey(unicode)
    user_name = Required(unicode)