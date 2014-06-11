# coding: utf-8
import copy
from Library import flaskhelper
from Library.flaskhelper import getargs
from Library.minihelper import getGridData, saveData

from flask import Blueprint,g
from flask.ext.login import login_required
from flask.templating import render_template
from pony.orm import *
from autodb.Logic.PermissionLogic import log


sql_list = Blueprint("sql_list", __name__)



@sql_list.route('/sqllistdata/', methods=['GET', 'POST'])
@db_session
@login_required
@log
def sqllistdata():

    from autodb.models.sqllist import sqllist
    from autodb.models.sqlresult import sqlresult



    data = select( p for p in sqllist  if p.user_code== g.user.user_code)



    return getGridData(entity=sqllist, data=data)


@sql_list.route('/sqlresult/', methods=['GET', 'POST'])
@db_session
@login_required
def sqlresult():
    '''
    获取sqlresult数据
    '''


    sguid=getargs("sguid")

    from autodb.models.sqlresult import sqlresult


    data=select(p for p in sqlresult if p.sguid==sguid ).order_by(desc(sqlresult.guid))
    return getGridData(sqlresult,data=data)




@sql_list.route('/sqllist/', methods=['GET', 'POST'])
@sql_list.route('/sqllist/<int:page>', methods=['GET', 'POST'])
@login_required
@log
def sqllist(page=1):
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
    saveData(sqllist, data)
    return "ok"