# -*- coding: utf8 -*-
import sys

import config
from flask import Flask
from flask_login import LoginManager


reload(sys)
sys.setdefaultencoding('utf-8')  #解决utf8编码问题

app = Flask(__name__)
app.config.from_object(config)

app.debug = False

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'user.login'
lm.login_message = unicode('请先登录', 'utf-8')


#加载model,生成maping
import models
#加载views,注册blueprint
import views



