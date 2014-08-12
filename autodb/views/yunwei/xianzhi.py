# coding: utf-8
from Library import flaskhelper
from Library.flaskhelper import getargs, isGetMethod
from Library.minihelper import getGridData, saveData
from autodb import cache

from flask import Blueprint, g, session
from flask.ext.login import login_required
from flask.templating import render_template
from pony.orm import *
from autodb.Logic.PermissionLogic import power,IsAdmin

xianzhi = Blueprint("xianzhi", __name__)


@xianzhi.route('/index', methods = ['GET', 'POST'])
@db_session
@power
def index() :
    '''
    运维闲置资源管理
    :return:
    '''
    isadmin=IsAdmin('系统管理员')
    #TODO:根据角色不同，控制不同的菜单及列的显示
    if isGetMethod() :
        return render_template("yunwei/xianzhi.html", isadmin= isadmin)
    from autodb.models.yunwei import xianzhi
    zcbh=getargs('zcbh')
    #按资产编号进行查询
    if zcbh:
        data = select(p for p in xianzhi if p.zcbh==zcbh).order_by(desc(xianzhi.guid))
    else:
        data=select(p for p in xianzhi).order_by(desc(xianzhi.guid))

    return getGridData(entity= xianzhi,data=data)


@xianzhi.route('/save', methods = ['POST'])
@db_session
@login_required
@power
def save() :
    '''
    运维闲置资源--保存闲置资源信息
    :return:
    '''
    from autodb.models.yunwei import xianzhi

    data = flaskhelper.getargs2json("data")

    #用户信息
    uinfo = { "topdpt" : session['topdpt'] }
    for x in data :
        if (x['_state']=="added"):
            #只有新增数据时填写更新信息
            x.update(uinfo)  # 更新用户信息

    if data :

        saveData(xianzhi, data, operator = g.user.user_code)
    return "操作完成"