# coding: utf-8
'''
文件作用:根目录下得基本文件
'''
from flask import Blueprint,session

from flask.templating import render_template
from pony.orm import *
root = Blueprint("root", __name__)


@root.route('/', methods=['GET', 'POST'])
@root.route('/index', methods=['GET', 'POST'])
def index():
    # from wiz.Logic.wizlogic import startmain
    #
    # invite_code = 'e42ad138'  #zihu
    # counts=10
    # startmain(invite_code, counts)
    from  wiz.models.invite_list import invite_list
    print(invite_list.__dict__)
    return render_template("index.html")


@root.route('/getproxy', methods=['GET', 'POST'])
def getproxy():
    from wiz.Logic.getproxy import getPageList

    getPageList(file='2120.html')
    return render_template("index.html")