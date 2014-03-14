#-*- coding:utf8
#from wtforms.ext.i18n.form import Form
from flask_wtf import Form
from wtforms.validators import Required
from wtforms.fields.simple import TextField
from wtforms.fields.core import BooleanField
from wtforms.ext.i18n.form import Form as w


class BaseForm(w, Form):
    LANGUAGES = ['zh']


class LoginForm(BaseForm):
    staffid = TextField('系统工号', validators=[Required()])
    remember_me = BooleanField('记住', default=False)


class WizStartForm(BaseForm):
    usercode = TextField('邀请码', validators=[Required()])
    counts = TextField('数目', validators=[Required()], default='20')


class WechatUserVeForm(BaseForm):
    usercode = TextField('门户账户', validators=[Required()])
    code = TextField('验证码', validators=[Required()])
    source = TextField('source')