# coding: utf-8
'''
description:
Created by weibaohui on 14-6-8.

'''
from decimal import Decimal
from autodb.Logic.Oracledb import db
from pony.orm import *


class EXT_CHART_GW_MXSR(db.Entity):
    '''
    固网单项明细
    '''
    ZHANGQI = Required(unicode)
    AREA_NAME= Optional(unicode)
    DATATYPE= Optional(unicode)
    SHOURU=Optional(unicode)

class EXT_CHART_GW_SQSH(db.Entity) :
    '''
    固网税前税后表
    '''
    ZHANGQI = Required(unicode)
    AREA_NAME = Optional(unicode)
    DATATYPE = Optional(unicode)
    SHUIQIAN = Optional(unicode)
    SHUIHOU = Optional(unicode)
    SHUILV = Optional(unicode)


class TMP_SHOURU_GUWANG(db.Entity):
    '''
    固网收入单项明细临时导入表
    '''
    orders = Optional(unicode)

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

class TMP_SHOURU_SQSH(db.Entity):
    '''
    固网税前税后导入临时表
    '''
    orders = Optional(unicode)
    sjly = Optional(unicode)
    sl = Optional(unicode)
    dys_h = Optional(Decimal)
    dys_q = Optional(Decimal)
    kfq_h = Optional(Decimal)
    kfq_q = Optional(Decimal)
    dyq_h = Optional(Decimal)
    dyq_q = Optional(Decimal)
    gr_h = Optional(Decimal)
    gr_q = Optional(Decimal)
    kl_h = Optional(Decimal)
    kl_q = Optional(Decimal)
    lj_h = Optional(Decimal)
    lj_q = Optional(Decimal)
    hkq_h = Optional(Decimal)
    hkq_q = Optional(Decimal)
    sz_h = Optional(Decimal)
    sz_q = Optional(Decimal)
    sn_h = Optional(Decimal)
    sn_q = Optional(Decimal)
    sb_h = Optional(Decimal)
    sb_q = Optional(Decimal)
    sd_h = Optional(Decimal)
    sd_q = Optional(Decimal)
    xh_h = Optional(Decimal)
    xh_q = Optional(Decimal)
    bz_h = Optional(Decimal)
    bz_q = Optional(Decimal)
    cl_h = Optional(Decimal)
    cl_q = Optional(Decimal)
    gd_h = Optional(Decimal)
    gd_q = Optional(Decimal)
    slhk_h = Optional(Decimal)
    slhk_q = Optional(Decimal)
    lp_h = Optional(Decimal)
    lp_q = Optional(Decimal)
    xyfwzx_h = Optional(Decimal)
    xyfwzx_q = Optional(Decimal)
    jkyb_h = Optional(Decimal)
    jkyb_q = Optional(Decimal)
    jkeb_h = Optional(Decimal)
    jkeb_q = Optional(Decimal)
    dcqd_h = Optional(Decimal)
    dcqd_q = Optional(Decimal)
    xcqd_h = Optional(Decimal)
    xcqd_q = Optional(Decimal)
    sbb_h = Optional(Decimal)
    sbb_q = Optional(Decimal)

