# coding: utf-8
import copy
from Library import flaskhelper
from Library.flaskhelper import getargs
from Library.minihelper import getGridData, saveData

from flask import Blueprint,g
from flask.ext.login import login_required
from flask.templating import render_template
from pony.orm import *



sql_list = Blueprint("sql_list", __name__)


@sql_list.route('/sqllistdata/', methods=['GET', 'POST'])
@db_session
@login_required
def sqllistdata():

    from autodb.models.sqllist import sqllist
    from autodb.models.sqlresult import sqlresult

    data= select((p.title,x.sguid,p.guid,p.nextexec,p.lastexec) for p in sqllist for x in sqlresult if  p.guid==x.sguid)


    #data = select( p for p in sqllist  if p.user_code== g.user.user_code)



    return getGridData( data=data)


@sql_list.route('/sqlresult/', methods=['GET', 'POST'])
@db_session
@login_required
def sqlresult():
    '''
    获取sqlresult数据
    '''


    sguid=getargs("sguid")

    from autodb.models.sqlresult import sqlresult


    data=select(p for p in sqlresult if p.sguid==sguid )
    total=select(count(p.guid) for p in sqlresult if p.sguid==sguid).first()
    return getGridData(sqlresult,data=data,total=total)




@sql_list.route('/sqllist/', methods=['GET', 'POST'])
@sql_list.route('/sqllist/<int:page>', methods=['GET', 'POST'])
@login_required
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