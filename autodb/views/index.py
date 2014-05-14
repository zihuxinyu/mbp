# coding: utf-8
'''
文件作用:根目录下得基本文件
'''
from flask import Blueprint

from flask_login import login_required
from flask.templating import render_template

root = Blueprint("root", __name__)
@root.route('/', methods=['GET', 'POST'])
@root.route('/index', methods=['GET', 'POST'])
@login_required
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
