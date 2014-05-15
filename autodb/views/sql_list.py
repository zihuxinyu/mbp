# coding: utf-8
from Library.flaskhelper import getargs
from Library.minihelper import getGridData
from flask import Blueprint
from flask.ext.login import login_required
from flask.templating import render_template
from pony.orm import *

sql_list = Blueprint("sql_list", __name__)


@sql_list.route('/sqllistdata/', methods=['GET', 'POST'])
@db_session
@login_required
def sqllistdata():
    from autodb.models.sqllist import sqllist

    pageIndex = int(getargs("pageIndex", 0))
    pageSize = int(getargs("pageSize", 0))

    total = select(count(p.guid) for p in sqllist).first()
    data = select(p for p in sqllist).limit(pageSize, pageSize * pageIndex)
    return getGridData(sqllist, total, data)


@sql_list.route('/sqlresult/', methods=['GET', 'POST'])
@db_session
@login_required
def sqlresult():
    '''
    获取sqlresult数据
    '''

    pageIndex =int( getargs( "pageIndex", 0))
    pageSize =int( getargs( "pageSize", 0))
    sguid=getargs("sguid")
    from autodb.models.sqlresult import sqlresult

    total=select(count(p.guid) for p in sqlresult if p.sguid == sguid).first()
    data=select(p for p in sqlresult if p.sguid==sguid).order_by(desc(sqlresult.opdate)).limit(pageSize,pageSize*pageIndex)
    return getGridData(sqlresult,total,data)




@sql_list.route('/sqllist/', methods=['GET', 'POST'])
@sql_list.route('/sqllist/<int:page>', methods=['GET', 'POST'])
@login_required
def sqllist(page=1):
    """
    sql列表

    :return:
    """

    return render_template('sqllist.html')