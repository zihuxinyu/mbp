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

    return render_template("index.html")


