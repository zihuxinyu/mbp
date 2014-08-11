# coding: utf-8
'''
description:
Created by weibaohui on 14-8-11.

'''
from autodb.Logic.Mysqldb import db
from pony.orm import *
from datetime import datetime


class xianzhi(db.Entity):
    '''
    运行维护部闲置板卡、设备信息
    '''
    _table_="yw_xianzhi"
    guid = PrimaryKey(int, auto = True)
    modifierid = Optional(unicode)
    modifydate = Optional(datetime, default = datetime.now())
    creatorid = Optional(unicode)
    createdate = Optional(datetime, default = datetime.now())

    zcbh = Optional(unicode)  # 资产编号
    zy = Optional(unicode)  # 专业
    cj = Optional(unicode)  # 厂家
    sbmc = Optional(unicode)  # 设备名称
    sbxh = Optional(unicode)  # 设备型号
    bkmc = Optional(unicode)  # 板卡名称
    bkxh = Optional(unicode)  # 板卡型号
    sbzt = Optional(unicode)  # 设备状态
    whx = Optional(unicode)  # 完好性
    bfzt = Optional(unicode)  # 报废状态
    dyzt = Optional(unicode)  # 调用状态
    zcssbm = Optional(unicode)  # 资产所属部门
    fzwz = Optional(unicode)  # 放置位置
    fzwzssdw = Optional(unicode)  #放置位置所属单位