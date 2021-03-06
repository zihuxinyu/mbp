# coding: utf-8
from Library import flaskhelper
from Library.flaskhelper import getargs
from Library.minihelper import getGridData, saveData
from autodb import cache

from flask import Blueprint, g, session
from flask.ext.login import login_required
from flask.templating import render_template
from pony.orm import *
from autodb.Logic.PermissionLogic import power

sql_list = Blueprint("sql_list", __name__)


@sql_list.route('/sqllistdata', methods=['GET', 'POST'])
@db_session
@login_required
@cache.memoize(2)
def sqllistdata():

    from autodb.models.sqllist import sqllist

    data = select(p for p in sqllist if p.user_code == g.user.user_code)

    return getGridData(entity=sqllist, data=data)


@sql_list.route('/sqlresult', methods=['GET', 'POST'])
@db_session
@login_required
@cache.memoize(2)
def sqlresult():
    '''
    获取sqlresult数据
    '''

    sguid = getargs("sguid")

    from autodb.models.sqlresult import sqlresult

    data = select(p for p in sqlresult if p.sguid == sguid).order_by(desc(sqlresult.guid))
    return getGridData(sqlresult, data=data)


@sql_list.route('/sqllist', methods=['GET', 'POST'])
@login_required
@power
def sqllist():
    """
    sql列表

    :return:
    """


    return render_template('sqllist.html')


@sql_list.route('/save/', methods=['GET', 'POST'])
@db_session
@login_required
def save():
    from autodb.models.sqllist import sqllist

    data = flaskhelper.getargs2json("data")


    saveData(sqllist, data, operator=g.user.user_code)
    return "数据保存成功"