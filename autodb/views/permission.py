# coding: utf-8
'''
文件作用:user相关操作
'''
from Library import flaskhelper
from Library.minihelper import saveData
from flask_login import login_required
from flask import Blueprint,g
from flask.templating import render_template
from Library.flaskhelper import getargs
from Library.minihelper import getGridData
from pony.orm import *

from autodb.Logic.PermissionLogic import geturlmap

permission = Blueprint("permission", __name__)


@permission.route('/reg')
@db_session
def reg():
    """
    自动注册所有模块

    """

    from autodb.models.portal import modulelist

    #将现有module设置为不可用
    data = select(p for p in modulelist)
    for d in data:
        modulelist.get(modulename=d.modulename).set(state="no")
    #重新获取现有路由，并注册
    rus = geturlmap()
    for x in rus:
        print(type(rus[x]['doc']))
        doc = rus[x]['doc'].decode("utf8").split(':return:')[0] if rus[x]['doc'] else ""
        url = ';'.join(rus[x]['rule'])
        single = modulelist.get(modulename=x)
        if single:
            modulelist.get(modulename=x).set(url=url, doc=doc, state='ok')
        else:
            modulelist(modulename=x, url=url, doc=doc, state='ok')
    #删除无用module
    data = select(p for p in modulelist if p.state == "no")
    for d in data:
        modulelist.get(modulename=d.modulename).delete()
    return "注册完成"


@permission.route('/g_p_list', methods=['GET', 'POST'])
@db_session
def group_module():
    '''
    group_Module对应关系
    :return:
    '''
    modulename = getargs("modulename")
    getdata=getargs("getdata",method='GET')
    if not getdata:
        return render_template("permission.html")
    from autodb.models.portal import group_module as gm
    data=select(p for p in gm if p.modulename== modulename)
    return getGridData(entity=gm,data=data)


@permission.route('/index', methods=['GET', 'POST'])
@db_session
def index():
    '''
    获取模块列表
    :return:
    '''
    from autodb.models.portal import modulelist

    getdata = getargs("getdata", method='GET')
    if not getdata:
        return render_template("permission.html")

    data = select(p for p in modulelist).order_by(modulelist.modulename)
    return getGridData(entity=modulelist, data=data)

@permission.route('/save/', methods=['GET', 'POST'])
@db_session
@login_required
def save_g_m():
    '''
    保存模块角色对应关系
    :return:
    '''
    from autodb.models.portal import group_module

    data = flaskhelper.getargs2json("data")
    saveData(group_module, data,operator=g.user.user_code)
    return "ok"