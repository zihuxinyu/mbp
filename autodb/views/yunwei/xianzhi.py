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
