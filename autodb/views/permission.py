# coding: utf-8
'''
文件作用:user相关操作
'''
from Library import flaskhelper
from Library.minihelper import saveData
from flask_login import logout_user, login_user, login_required
from flask.helpers import url_for, flash
from flask import Blueprint,g
from flask.globals import request, session
from flask.templating import render_template
from Library.flaskhelper import getargs
from Library.minihelper import getGridData
from pony.orm import *
from sqlalchemy import update, delete

permission = Blueprint("permission", __name__)


@permission.route('/reg')
@db_session
def reg():
    """
    自动注册所有模块

    """

    from autodb.Logic.PermissionLogic import geturlmap
    from autodb.models.portal import modulelist

    rus = geturlmap()
    data = select(p for p in modulelist)
    for d in data:
        modulelist.get(module=d.module).set(state="no")
    for x in rus:
        print(type(rus[x]['doc']))
        doc = rus[x]['doc'].decode("utf8").split(':return:')[0] if rus[x]['doc'] else ""
        url = ';'.join(rus[x]['rule'])
        single = modulelist.get(module=x)
        if single:
            modulelist.get(module=x).set(url=url, doc=doc, state='ok')
        else:
            modulelist(module=x, url=url, doc=doc, state='ok')
    data = select(p for p in modulelist if p.state == "no")
    for d in data:
        modulelist.get(module=d.module).delete()
    return "注册完成"


@permission.route('/g_p_list', methods=['GET', 'POST'])
@db_session
def group_module():
    '''
    group_Module对应关系
    :return:
    '''
    mguid = getargs("mguid")
    getdata=getargs("getdata",method='GET')
    if not getdata:
        return render_template("permission.html")
    from autodb.models.portal import group_module as gm
    data=select(p for p in gm if p.moduleid==mguid)
    return getGridData(entity=gm,data=data)


@permission.route('/modulelist', methods=['GET', 'POST'])
@db_session
def modulelist():
    '''
    获取模块列表
    :return:
    '''
    getdata = getargs("getdata", method='GET')
    if not getdata:
        return render_template("permission.html")
    from autodb.models.portal import modulelist

    data = select(p for p in modulelist)
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