# coding: utf-8
'''
description:使用前将model加载,并生成map
Created by weibaohui on 14-5-14.

'''
from pony.orm import sql_debug
from wiz.Logic.Mysqldb import db

#注册model

import portal,wiz_user,invite_list,proxy_list,xiaomi,wiz_sell


#开启调试模式
sql_debug(False)
db.generate_mapping()
