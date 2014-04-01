#-*- coding:utf8
#from wtforms.ext.i18n.form import Form
from flask_wtf import Form
from wtforms.validators import Required
from wtforms.fields.simple import TextField
from wtforms.fields.core import BooleanField, SelectField, DateTimeField
from wtforms.ext.i18n.form import Form as w


class BaseForm(w, Form):
    LANGUAGES = ['zh']


class LoginForm(BaseForm):
    usercode = TextField('请输入门户账户', validators=[Required()])




class FMsqllist(BaseForm):
    title = TextField('title')
    sqlContent = TextField('sqlContent')
    paras = TextField('paras')
    frequency = SelectField('frequency')
    #lastexec = DateTimeField('lastexec')
    #nextexec = DateTimeField('nextexec')
    user_code = TextField('user_code')
    #opdate = DateTimeField('opdate')
