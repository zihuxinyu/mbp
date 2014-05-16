# coding: utf-8
from Library import flaskhelper
from Library.flaskhelper import getargs
from Library.minihelper import getGridData, saveData
from flask import Blueprint
from flask.ext.login import login_required
from flask.templating import render_template
from pony.orm import *
from wiz.models.proxy_list import proxy_list
import json

proxylist = Blueprint("proxylist", __name__)


@proxylist.route('/proxyresult/', methods=['GET', 'POST'])
@db_session
@login_required
def proxyresult():
    '''
    获取proxyresult数据
    '''

    pageIndex = int(getargs("pageIndex", 0))
    pageSize = int(getargs("pageSize", 0))

    total = select(count(p.guid) for p in proxy_list ).first()
    data = select(p for p in proxy_list ) \
        .order_by(desc(proxy_list.state))\
        .order_by(desc(proxy_list.opdate))\
        .limit(pageSize,
                                                                                                             pageIndex)
    return getGridData(proxy_list, total, data)


@proxylist.route('/getproxy/', methods=['GET', 'POST'])
def getproxy():
    '''
    开始
    '''
    from wiz.Logic.getproxy import getPageList
    from Library.flaskhelper import getargs
    file=getargs('key','2120')
    getPageList(file=file+'.html')
    return "ok"


@proxylist.route('/list/', methods=['GET', 'POST'])
@login_required
def list(page=1):
    return render_template('proxylist.html')


@proxylist.route('/save/', methods=['GET', 'POST'])
@login_required
@db_session
def save():
    data = flaskhelper.getargs("data")
    data = json.loads(data)
    saveData(proxy_list, data)
    return "ok"
