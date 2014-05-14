# coding: utf-8
# coding: utf-8
'''
文件作用:注册route,注册全局方法
'''
from autodb import app
from autodb.modelx import portal_user
from flask import g, render_template
from sql_list import sql_list
from  login import user
from index import root
from  autodb import lm
from flask_login import current_user

app.register_blueprint(root)
app.register_blueprint(sql_list, url_prefix='/sql')
app.register_blueprint(user, url_prefix='/user')


@lm.user_loader
def load_user(id):
    return portal_user.query.filter(portal_user.user_code == id).first()


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