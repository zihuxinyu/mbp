# coding: utf-8
from  flask import  request,session
from flask.ext.babelex import Babel
from mbp import  app,db
from flask.ext.admin import Admin
from mbp.manage.views import MissionBarcode,MissionUser,Mission,UserGroup

babel = Babel(app)
admin = Admin(app,name='后台管理')

admin.add_view(UserGroup(db.session, category='用户角色', name='用户角色管理'))

admin.add_view(Mission(db.session, category='清查任务', name='核查任务管理'))
admin.add_view(MissionBarcode(db.session, category='清查任务', name='核查资产标签管理'))
admin.add_view(MissionUser(db.session, category='清查任务', name='核查人员管理'))


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