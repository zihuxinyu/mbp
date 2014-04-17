#-*- coding:utf8
#from wtforms.ext.i18n.form import Form
from flask_wtf import Form
from wtforms.validators import Required
from wtforms.fields.simple import TextField
from wtforms.fields.core import BooleanField, SelectField, DateTimeField,DateField
from wtforms.ext.i18n.form import Form as w


class BaseForm(w, Form):
    LANGUAGES = ['zh']


class LoginForm(BaseForm):
    usercode = TextField('请输入营业账户', validators=[Required()])





class WechatUserSendcode(BaseForm):
    usercode = TextField('请输入营业账户', validators=[Required()])
class WechatChkCode(BaseForm):
    code=TextField('请输入验证码',validators=[Required()])


class SearchForm(BaseForm):
    startdate = DateField('起始时间', validators=[Required()])
    enddate = DateField('结束时间', validators=[Required()])

