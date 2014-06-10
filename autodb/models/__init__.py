# coding: utf-8
'''
description:使用前将model加载,并生成map
Created by weibaohui on 14-5-14.

'''
from pony.orm import sql_debug
from autodb.Logic.Mysqldb import db
from autodb.Logic.Oracledb import db as odb
#注册model

import portal, sqllist, sqlresult,EXT_DPT_USR,GUWANG


#开启调试模式
sql_debug(True)
db.generate_mapping()
odb.generate_mapping()