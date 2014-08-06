# -*- coding: utf8 -*-
import sys

import config
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_cache import Cache
reload(sys)
sys.setdefaultencoding('utf-8')  #解决utf8编码问题

app = Flask(__name__)
app.config.from_object(config)

app.debug = True

cache = Cache(app,config={'CACHE_TYPE':"redis",
                          "CACHE_REDIS_HOST":"134.44.36.125",
                          "CACHE_REDIS_PORT":"6379",
"CACHE_REDIS_PASSWORD":"%$s%dd$%d#s^df#$a^fd%sf*^&(d*d&^)gh*^jk*e(*&e*s#%",
                          "CACHE_REDIS_DB":"0",
                          "CACHE_KEY_PREFIX":"Logic"})

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'user.login'
lm.login_message = unicode('请先登录', 'utf-8')


#加载model,生成maping
import models
#加载views,注册blueprint
import views


