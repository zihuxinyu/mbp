# coding: utf-8
'''
文件作用:根目录下得基本文件
'''
from autodb import  cache
from flask import Blueprint,session

from flask.templating import render_template
from pony.orm import *
root = Blueprint("root", __name__)


@cache.memoize(10)
@root.route('/', methods=['GET', 'POST'])
@root.route('/index', methods=['GET', 'POST'])
def index():
    return render_template("index.html")


@root.route('/cs/<tablename>')
def cs(tablename):
    """
    输入表名,生成MODEL
    :param tablename:
    :return:
    """
    from autodb.config import DB_DATEBASE
    from autodb import  db
    sql = "SELECT `COLUMN_NAME`,`DATA_TYPE`,`EXTRA`,`COLUMN_COMMENT` FROM information_schema.columns WHERE table_schema='{0}' AND " \
          "table_name='{1}'".format(DB_DATEBASE, tablename)
    cur = db.engine.execute(sql)
    entries = [dict(COLUMN_NAME=row[0], DATA_TYPE=row[1], EXTRA=row[2], COLUMN_COMMENT=row[3]) for row in
               cur.fetchall()]

    return render_template('cs.html', list=entries, tablename=tablename)

@cache.memoize(10)
@root.route('/daohang')
def daohang():
    return  render_template("daohang.html")


@root.route('/menutree')
def menutree():
    s='''
    [
	{id: "lists", text: "自动任务管理"},

	{id: "sqllist", text: "任务列表", pid: "lists" ,url:'/sql/sqllist/'},

	{id: "datagrid", text: "DataGrid", pid: "lists"},
	{id: "tree", text: "Tree" , pid: "datagrid"},
	{id: "treegrid", text: "TreeGrid " , pid: "datagrid"},

	{id: "layouts", text: "Layouts", pid: "user"},

	{id: "panel", text: "Panel", pid: "layouts"},
	{id: "splitter", text: "Splitter", pid: "layouts"},
	{id: "layout", text: "Layout ", pid: "layouts"},

	{ id: "right", text: "权限管理"},

	{id: "base", text: "Base",  pid: "right" },

	{id: "ajax", text: "Ajax", pid: "base"},
	{id: "json", text: "JSON", pid: "base"},
	{id: "date", text: "Date", pid: "base"},

	{id: "forms", text: "Forms", pid: "right"},

	{id: "button", text: "Button", pid: "forms"},
	{id: "listbox", text: "ListBox", pid: "forms"},
	{id: "checkboxlist", text: "CheckBoxList", pid: "forms"},
	{id: "radiolist", text: "RadioList", pid: "forms"},
	{id: "calendar", text: "Calendar", pid: "forms"}
]



    '''

    return s