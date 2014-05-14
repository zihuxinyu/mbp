# coding: utf-8
'''
description:产生Mysql pony db
Created by weibaohui on 14-5-14.

'''

from pony.orm import *
from  autodb.config import DB_DATEBASE,DB_HOST,DB_PSW,DB_USER
db = Database('mysql', host=DB_HOST, user=DB_USER, passwd=DB_PSW, db=DB_DATEBASE)

sql_debug(True)



