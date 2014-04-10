# coding: utf-8
from  flask import  request,session
from flask.ext.babelex import Babel
from mbp import  app,db
from flask.ext.admin import Admin
from mbp.manage.views import MyView,MissionBarcode
from flask.ext.admin.contrib.sqla import ModelView
from mbp.models import mission as Mmission

babel = Babel(app)
admin = Admin(app)

admin.add_view(ModelView(Mmission, db.session, category='核查任务', name='任务管理'))
admin.add_view(MissionBarcode(db.session, category='核查任务', name='资产标签管理' ))


@babel.localeselector
def get_locale():

    """
    设置语言

    :return:
    """
    override = request.args.get('lang')

    if override:
        session['lang'] = override

    return session.get('lang', 'zh')