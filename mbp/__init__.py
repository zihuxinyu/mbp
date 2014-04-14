# -*- coding: utf8 -*-
import sys

from flask import Flask, render_template

from flask_login import LoginManager
from Library.config import basedir, WEROBOT_TOKEN

from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask.ext.werobot import WeRoBot

reload(sys)
sys.setdefaultencoding('utf-8')  #解决utf8编码问题

app = Flask(__name__)
app.config.from_pyfile(basedir+'/config.py')
app.debug = True
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
lm.login_message = unicode('请先登录', 'utf-8')
#CsrfProtect(app)
mail = Mail(app)
db = SQLAlchemy(app)

#初始化管理
import mbp.manage



robot = WeRoBot(app, token=WEROBOT_TOKEN, enable_session=True)


from mbp import views


@app.errorhandler(404)
def internal_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    #db.session.rollback()
    return render_template('500.html'), 500


