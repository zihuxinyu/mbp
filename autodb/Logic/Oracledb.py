# coding: utf-8
'''
description:产生Mysql pony db
Created by weibaohui on 14-5-14.

'''

import cx_Oracle

from pony.orm import *
from Library.config import O_host, O_port, O_database, O_user, O_password


dsn = cx_Oracle.makedsn(O_host, O_port, O_database)

db = Database('oracle', O_user, O_password, dsn)


