  # coding: utf-8

from autodb.Logic.DBLogic import AdoHelper
from Library.minihelper import getData
from flask import Blueprint
from flask.globals import request

from flask.templating import render_template

sql_list = Blueprint("sql_list", __name__
)


@sql_list.route('/sqllistdata/', methods=['GET', 'POST'])
def sqllistdata():
    '''
    获取sqllist数据
    pageIndex	0
pageSize	10
sortField	createtime
sortOrder	desc
    '''

    pageIndex = int(request.form["pageIndex"]) if request.form["pageIndex"] else 0;
    pageSize = int(request.form["pageSize"]) if request.form["pageSize"] else 3;

    sql = "select * from sqllist";
    sqlwhere = " 1";

    return getData(sql, sqlwhere, pageSize, pageIndex, AdoHelper().db())


@sql_list.route('/sqlresult/', methods=['GET', 'POST'])
def sqlresult():
    '''
    获取sqlresult数据
    '''

    pageIndex = int(request.form["pageIndex"]) if request.form["pageIndex"] else 0;
    pageSize = int(request.form["pageSize"]) if request.form["pageSize"] else 3;
    sguid = request.form["sguid"]

    sql = "select * from sqlresult";
    if sguid:
        sqlwhere = " sguid='{0}' order by guid desc".format(sguid);

        return getData(sql, sqlwhere, pageSize, pageIndex, AdoHelper().db())


@sql_list.route('/sqllist/', methods=['GET', 'POST'])
@sql_list.route('/sqllist/<int:page>', methods=['GET', 'POST'])
def sqllist(page=1):
    """
    sql列表

    :return:
    """

    return render_template('sqllist.html')