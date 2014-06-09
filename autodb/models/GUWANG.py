# coding: utf-8
'''
description:
Created by weibaohui on 14-6-8.

'''
from decimal import Decimal
from autodb.Logic.Oracledb import db
from pony.orm import *


class EXT_CHART_GW_MXSR(db.Entity):

    ZHANGQI = Required(unicode)
    AREA_NAME= Optional(unicode)
    DATATYPE= Optional(unicode)
    SHOURU=Optional(unicode)

class TMP_SHOURU_GUWANG(db.Entity):
    sjly = Optional(unicode)
    kfq = Optional(Decimal)
    dyq = Optional(Decimal)
    gr = Optional(Decimal)
    kl = Optional(Decimal)
    lj = Optional(Decimal)
    hkq = Optional(Decimal)
    sz = Optional(Decimal)
    sn = Optional(Decimal)
    sb = Optional(Decimal)
    sd = Optional(Decimal)
    xh = Optional(Decimal)
    bz = Optional(Decimal)
    cl = Optional(Decimal)
    gd = Optional(Decimal)
    slhk = Optional(Decimal)
    lp = Optional(Decimal)
    xyfwzx = Optional(Decimal)
    jkyb = Optional(Decimal)
    jkeb = Optional(Decimal)
    dcqd = Optional(Decimal)
    xcqd = Optional(Decimal)
    sbb = Optional(Decimal)
