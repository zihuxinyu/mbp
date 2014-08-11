# coding: utf-8
from Library import flaskhelper
from Library.flaskhelper import getargs, isGetMethod
from Library.minihelper import getGridData, saveData
from autodb import cache

from flask import Blueprint, g, session
from flask.ext.login import login_required
from flask.templating import render_template
from pony.orm import *
from autodb.Logic.PermissionLogic import power

xianzhi = Blueprint("xianzhi", __name__)


@xianzhi.route('/index', methods = ['GET', 'POST'])
@db_session
def index() :
    '''
    获取模块列表
    :return:
    '''


    if isGetMethod() :
        return render_template("yunwei/xianzhi.html")
    from autodb.models.yunwei import xianzhi
    data=select(p for p in xianzhi).order_by(desc(xianzhi.guid))

    return getGridData(entity= xianzhi,data=data)


@xianzhi.route('/save', methods = ['POST'])
@db_session
@login_required
@power
def save() :
    '''
    保存闲置资源信息
    :return:
    '''
    # from autodb.models.portal import group_module
    #
    # data = flaskhelper.getargs2json("data")
    # if data :
    #     saveData(group_module, data, operator = g.user.user_code)
    return "操作完成"