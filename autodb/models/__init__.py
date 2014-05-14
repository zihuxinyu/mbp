# coding: utf-8
'''
description:使用前将model加载,并生成map
Created by weibaohui on 14-5-14.

'''
from pony.orm import sql_debug
from autodb.Logic.Mysqldb import db

#注册model
from autodb.models.sqlresult import sqlresult
from autodb.models.sqllist import sqllist

sql_debug(True)
db.generate_mapping()
