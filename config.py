# -*- coding: utf8 -*-
import os

basedir = os.path.abspath(os.path.dirname(__file__))
CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'
DEBUG_TB_INTERCEPT_REDIRECTS = False

#Mysql
SQLALCHEMY_DATABASE_URI = 'mysql://root:root@127.0.0.1/DLS'
SQLALCHEMY_ECHO = True

# email server
MAIL_SERVER = 'smtp.126.com'
MAIL_PORT = 25
MAIL_USE_TLS = False
MAIL_USE_SSL = False
MAIL_USERNAME = 'aixinit'
MAIL_PASSWORD = '9Loveme?'

WEROBOT_TOKEN = '08560a699966442fae5b3a165c0f8f71'
WEROBOT_ROLE = '/wechat'

# administrator list
ADMINS = ['aixinit@126.com']

# pagination
POSTS_PER_PAGE = 10
MAX_SEARCH_RESULTS = 50
