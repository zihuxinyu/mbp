# coding: utf-8
from Library import flaskhelper
from Library.flaskhelper import getargs, isGetMethod
from Library.minihelper import getGridData, saveData

from flask import Blueprint, g, session
from flask.ext.login import login_required
from flask.templating import render_template
from pony.orm import *
from autodb.Logic.PermissionLogic import power, IsAdmin

xianzhi = Blueprint("xianzhi", __name__)


@xianzhi.route('/index', methods = ['GET', 'POST'])
@db_session
@power
def index() :
    '''
    运维闲置资源管理
    :return:
    '''
    # 此模块的管理员角色名称
    isadmin = IsAdmin(['系统管理员', '运维闲置资产管理市分'])
    if isGetMethod() :
        return render_template("yunwei/xianzhi.html", isadmin = isadmin)
    from autodb.models.yunwei import xianzhi

    zcbh = getargs('zcbh')
    topdpt = session['topdpt']
    print(topdpt)

    #按资产编号进行查询
    vsql = "p for p in xianzhi if True "
    if zcbh :
        vsql += " and p.zcbh=='{0}'".format(zcbh)
    if not isadmin:
        #不是管理员加限制
        vsql+=" and p.creatorid=='{0}'".format(g.user.get_id())

    data = select(vsql).order_by(desc(xianzhi.guid))

    return getGridData(entity = xianzhi, data = data)


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

    # 用户信息
    uinfo = { "topdpt" : session['topdpt'] }
    for x in data :
        if (x['_state'] == "added") :
            #只有新增数据时填写更新信息
            x.update(uinfo)  # 更新用户信息

    if data :

        saveData(xianzhi, data, operator = g.user.user_code)
    return "操作完成"