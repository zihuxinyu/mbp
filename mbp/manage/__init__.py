__author__ = 'weibaohui'
# coding: utf-8
from mbp import  app,db
from flask.ext.admin import Admin
from mbp.manage.views import MyView,MissionBarcode
from flask.ext.admin.contrib.sqla import ModelView
from mbp.models import mission as Mmission

admin = Admin(app)
admin.add_view(MyView(name='Hello 1', endpoint='test1', category='Test'))
admin.add_view(MyView(name='Hello 2', endpoint='test2', category='Test'))
admin.add_view(MyView(name='Hello 3', endpoint='test3', category='Test'))
admin.add_view(ModelView(Mmission, db.session, category='核查任务', name='任务管理'))
admin.add_view(MissionBarcode(db.session, category='核查任务', name='资产标签管理',))
