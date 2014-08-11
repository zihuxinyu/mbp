# coding: utf-8
'''
文件作用:注册route,注册全局方法
'''
from autodb import app
from flask import g, render_template, session
from permission import permission
from sql_list import sql_list
from login import user
from root import root
from autodb import lm
from flask_login import current_user
from autodb.models.portal import users
from yunwei.xianzhi import xianzhi
from autodb import cache

#根目录访问路径
app.register_blueprint(root)
#自动任务执行
app.register_blueprint(sql_list, url_prefix = '/sql')
#用户管理
app.register_blueprint(user, url_prefix = '/user')
#权限管理
app.register_blueprint(permission, url_prefix = '/p')
#运维管理
app.register_blueprint(xianzhi, url_prefix = '/yunwei/xianzhi')


from pony.orm import *


@lm.user_loader
@db_session
@cache.memoize()
def load_user(id) :
    return users(id)


@app.before_request
def before_request() :
    g.user = current_user
    g.s = session


@app.errorhandler(404)
def internal_error(error) :
    return render_template('404.html'), 404


@app.errorhandler(403)
def internal_error(error) :
    return render_template('403.html', user_code = g.user.get_id()), 403


@app.errorhandler(500)
def internal_error(error) :
    # db.session.rollback()
    return render_template('500.html'), 500