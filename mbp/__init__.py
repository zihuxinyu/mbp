# -*- coding: utf8 -*-
import sys

from flask import Flask, render_template
from flask.ext.debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager
from config import ADMINS, MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD
from flask_wtf.csrf import CsrfProtect
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask.ext.werobot import WeRoBot

reload(sys)
sys.setdefaultencoding('utf-8')  #解决utf8编码问题

app = Flask(__name__)
app.config.from_object('config')
app.debug = True
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
lm.login_message = unicode('请先登录', 'utf-8')
#CsrfProtect(app)
mail = Mail(app)
db = SQLAlchemy(app)
toolbar = DebugToolbarExtension(app)
robot = WeRoBot(app,token='08560a699966442fae5b3a165c0f8f71',enable_session=True)


if not app.debug:
    import logging
    from logging.handlers import SMTPHandler

    credentials = None
    if MAIL_USERNAME or MAIL_PASSWORD:
        credentials = (MAIL_USERNAME, MAIL_PASSWORD)
    mail_handler = SMTPHandler((MAIL_SERVER, MAIL_PORT), 'no-reply@' + MAIL_SERVER, ADMINS, ' failure', credentials)
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)

if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler

    file_handler = RotatingFileHandler('tmp/log.log', 'a', 1 * 1024 * 1024, 10)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('mbp startup')

from mbp import views


@app.errorhandler(404)
def internal_error(error):
    return render_template('404.html'), 404


