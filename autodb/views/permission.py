# coding: utf-8
'''
文件作用:user相关操作
'''
from Library import flaskhelper
from Library.minihelper import saveData
from flask_login import login_required
from flask import Blueprint, g
from flask.templating import render_template
from Library.flaskhelper import getargs,isGetMethod
from Library.minihelper import getGridData,getTreeData

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

    # 将现有module设置为不可用
    data = select(p for p in modulelist)
    for d in data:
        modulelist.get(modulename=d.modulename).set(state="no")
    #重新获取现有路由，并注册
    rus = geturlmap()
    for x in rus:
        doc = rus[x]['doc'].decode("utf8").split('\n')[1] if rus[x]['doc'] else ""
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
    if isGetMethod():
        return render_template("permission.html")
    from autodb.models.portal import group_module as gm

    data = select(p for p in gm if p.modulename == modulename)
    return getGridData(entity=gm, data=data)


@permission.route('/index', methods=['GET', 'POST'])
@db_session
def index():
    '''
    获取模块列表
    :return:
    '''
    from autodb.models.portal import modulelist

    if isGetMethod():
        return render_template("permission.html")

    data = select(p for p in modulelist).order_by(modulelist.modulename)
    return getGridData(entity=modulelist, data=data)


@permission.route('/save', methods=['GET', 'POST'])
@db_session
@login_required
def save_g_m():
    '''
    保存模块角色对应关系
    :return:
    '''
    from autodb.models.portal import group_module

    data = flaskhelper.getargs2json("data")
    saveData(group_module, data, operator=g.user.user_code)
    return "ok"


@permission.route('/getMenu', methods=['GET', 'POST'])
@db_session
def getMenu():
    '''
    获取菜单列表
    :return:
    '''

    if isGetMethod() and getargs("getpage"):
        return render_template("menutree.html")

    from autodb.models.portal import menutree
    data=select(p for p in menutree ).order_by(menutree.num)

    return getTreeData(entity=menutree,data=data)




@permission.route('/savemenu', methods=['GET', 'POST'])
@db_session
@login_required
def savemenu():
    '''
    保存菜单
    :return:
    '''

    from autodb.models.portal import menutree

    operator = 'weibh'
    listdata=[]
    #需要新建、修改的数据
    data = flaskhelper.getargs2json("data")

    getlist(data,listdata)



    #删除的数据处理
    data = flaskhelper.getargs2json("removed")
    getlist(data, listdata)

    print("diedai:", listdata)

    saveData(menutree, listdata, operator=operator)
    return "ok"


def getlist(data, listdata):
    '''
    得到列表中得所有信息
    :param data:页面传过来的所有数据
    :param listdata:筛选出有增加或修改的数据
    :return:list,listdata
    '''
    for d in data:
        if "_state" in d:
            listdata.append(d)
        if "children" in d:
            #遍历
            getlist(d['children'],listdata)
