# coding: utf-8
'''
文件作用:user相关操作
'''
from Library import flaskhelper
from Library.minihelper import saveData
from flask_login import logout_user, login_user, login_required
from flask.helpers import url_for, flash
from flask import Blueprint
from flask.globals import request, session
from flask.templating import render_template
from Library.flaskhelper import getargs
from Library.minihelper import getGridData
from pony.orm import *

permission = Blueprint("permission", __name__)
@permission.route('/get', methods=['GET', 'POST'])
@db_session
def get():
    getdata=getargs("getdata",method='GET')
    print(getdata)
    if not getdata:
        return render_template("permission.html")
    from autodb.models.portal import group_module as gm
    data=select(p for p in gm)
    return getGridData(entity=gm,data=data)

@permission.route('/save/', methods=['GET', 'POST'])
@db_session
@login_required
def save():
    from autodb.models.sqllist import sqllist

    data = flaskhelper.getargs2json("data")
    saveData(sqllist, data)
    return "ok"