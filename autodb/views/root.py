# coding: utf-8
'''
文件作用:根目录下得基本文件
'''
from autodb import cache
from flask import Blueprint, g, session
from flask_login import login_required
from flask.templating import render_template
from pony.orm import *
from datetime import datetime, date

root = Blueprint("root", __name__)


@root.route('/', methods=['GET', 'POST'])
@root.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    return render_template("index.html",year= datetime.now().year)


@root.route('/cs/<tablename>')
def cs(tablename):
    """
    输入表名,生成MODEL
    :param tablename:
    :return:
    """
    from autodb.config import DB_DATEBASE

    sql = "SELECT `COLUMN_NAME`,`DATA_TYPE`,`EXTRA`,`COLUMN_COMMENT` FROM information_schema.columns WHERE " \
          "table_schema='{0}' AND " \
          "table_name='{1}'".format(DB_DATEBASE, tablename)
    # cur = db.engine.execute(sql)
    # entries = [dict(COLUMN_NAME=row[0], DATA_TYPE=row[1], EXTRA=row[2], COLUMN_COMMENT=row[3]) for row in
    # cur.fetchall()]

    # return render_template('cs.html', list=entries, tablename=tablename)
    #return ok


@cache.memoize(10)
@root.route('/daohang')
def daohang():
    return render_template("daohang.html")





@root.route('/shouru')
@db_session
def shouru():
    """
    固网收入格式整理，导入TMP_SHOURU_GUWANG

    :return:
    """
    from autodb.models.GUWANG import TMP_SHOURU_GUWANG as gw
    from autodb.Logic.ponyLogic import db

    zhangqi = '201408'
    tmp = "insert into   EXT_CHART_GW_MXSR t (ZHANGQI,AREA_NAME,DATATYPE,SHOURU ,orders) values ('{0}','{1}','{2}'," \
          "'{3}','{4}' ) ";
    xf = {"KFQ": "开发区", "DYQ": "东营区", "GR": "广饶县", "KL": "垦利县", "LJ": "利津县", "HKQ": "河口区", "SZ": "胜中分公司", "SN": "胜南分公司",
          "SB": "胜北分公司", "SD": "胜东分公司", "XH": "仙河分公司", "BZ": "胜利滨州分公司", "CL": "纯梁分公司", "GD": "孤岛分公司", "SLHK": "胜利河口分公司",
          "LP": "临盘分公司",
          "XYFWZX": "校园服务中心", "JKYB": "集团客户一部", "JKEB": "集团客户二部", "DCQD": "东城渠道服务中心", "XCQD": "西城渠道服务中心",
          "SBB": "东营市分公司"}

    db.execute("delete from EXT_CHART_GW_MXSR t where t.zhangqi='{0}'".format(zhangqi))
    data = select(p for p in gw)
    for d in data:
        if d.sjly:
            datas = select(x for x in gw if x.sjly == d.sjly)
            for ds in datas:
                for y in xf:
                    x = tmp.format(zhangqi, str(xf[y]), d.sjly, str(getattr(ds, str(y).lower())).replace("None", "0"),
                                   str(getattr(ds, 'orders')))
                    print(x)
                    db.execute(x)

    return "ok"


@root.route('/sqsh')
@db_session
def sqsh() :
    """
    固网收入税前税后对比格式

    :return:
    """
    from autodb.models.GUWANG import TMP_SHOURU_SQSH as sqsh
    from autodb.Logic.ponyLogic import db

    zhangqi = '201408'
    tmp = "insert into   EXT_CHART_GW_SQSH t (ZHANGQI,AREA_NAME,DATATYPE ,orders,shuiqian,shuihou,shuilv) values ('{0}','{1}','{2}'," \
          "'{3}','{4}' ,'{5}','{6}'  ) ";
    xf = { "KFQ" : "开发区",
           "DYQ" : "东营区",
           "GR" : "广饶县",
           "KL" : "垦利县",
           "LJ" : "利津县",
           "HKQ" : "河口区",
           "SZ" : "胜中分公司",
           "SN" : "胜南分公司",
           "SB" : "胜北分公司",
           "SD" : "胜东分公司",
           "XH" : "仙河分公司",
           "BZ" : "胜利滨州分公司",
           "CL" : "纯梁分公司",
           "GD" : "孤岛分公司",
           "SLHK" : "胜利河口分公司",
           "LP" : "临盘分公司",
           "XYFWZX" : "校园服务中心",
           "JKYB" : "集团客户一部",
           "JKEB" : "集团客户二部",
           "DCQD" : "东城渠道服务中心",
           "XCQD" : "西城渠道服务中心",
           "SBB" : "市本部",
           "DYS":"东营市分公司"}

    db.execute("delete from EXT_CHART_GW_SQSH t where t.zhangqi='{0}'".format(zhangqi))
    data = select(p for p in sqsh)
    for d in data :
        if d.sjly :
            datas = select(x for x in sqsh if x.sjly == d.sjly)
            for ds in datas :
                print(ds.sjly)
                for y in xf :
                    x = tmp.format(zhangqi, str(xf[y]), d.sjly, str(getattr(ds, 'orders')),
                                   str(getattr(ds, str(y+"_Q").lower())).replace("None", "0"),
                                   str(getattr(ds, str(y+"_H").lower())).replace("None", "0"),
                                   str(getattr(ds,'sl')).replace("None", "")

                                   )
                    print(x)
                    db.execute(x)

    return zhangqi+"ok"






