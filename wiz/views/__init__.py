# coding: utf-8
# coding: utf-8
'''
文件作用:注册route,注册全局方法
'''
from wiz import app
from flask import g, render_template
from  wiz.views.wizlist import wizlist
from wiz.views.proxy import proxylist
from  login import user
from root import root
from  wiz import lm
from flask_login import current_user
from pony.orm import *

app.register_blueprint(root)
app.register_blueprint(wizlist, url_prefix='/wiz')
app.register_blueprint(user, url_prefix='/user')
app.register_blueprint(proxylist, url_prefix='/proxy')


@lm.user_loader
@db_session
def load_user(id):
    from autodb.models.portal import  users
    return users(id)


@app.before_request
def before_request():
    g.user = current_user


@app.errorhandler(404)
def internal_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    #db.session.rollback()
    return render_template('500.html'), 500