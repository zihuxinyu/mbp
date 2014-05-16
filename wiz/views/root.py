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
    from wiz.models.proxy_list import proxy_list
    with db_session:
        select(p for p in proxy_list if "ddsf" not in  p.proxy).limit(1).show()
    return render_template("index.html")


@root.route('/getproxy', methods=['GET', 'POST'])
def getproxy():
    from wiz.Logic.getproxy import getPageList

    getPageList(file='2120.html')
    return render_template("index.html")