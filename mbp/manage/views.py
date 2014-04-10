# coding: utf-8
from flask.ext.admin import Admin, BaseView, expose
from flask import g
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.admin.form import rules
from markupsafe import Markup
from sqlalchemy.event import listens_for
from wtforms import SelectField
from mbp.models import mission_barcode


def _getMissionHref(view, context, model, name):
    return Markup("<a href='/index?mid={0}' target=_blank>{1}</a>".format(model.missionid, model.missionid))


class MyView(BaseView):
    def is_accessible(self):
        #认证通过的才能显示,可以自定义逻辑
        return g.user.is_authenticated()
    @expose('/')
    def index(self):
        return self.render('admin/index.html')


class MissionBarcode(ModelView):

    #edit_template = 'admin/edit.html'
    form_overrides = dict(missionid=SelectField)
    form_args = dict(
        # Pass the choices to the `SelectField`

        missionid=dict(
            choices=[('0', 'waiting'), ('1', 'in_progress'), ('2', 'finished')]
        ))

    form_create_rules = [
        rules.Header("dsdsdsd"),
        rules.HTML('''
        <font color=red>ddd</font>
        '''),

        rules.FieldSet(('missionid', 'barcode'), '任务信息'),

    ]


    column_formatters = {
        'missionid': _getMissionHref
    }
    #可以创建新的
    can_create = True

    #显示字段
    column_list = ('missionid', 'barcode')
    #设置过滤器
    column_filters = ('missionid', 'barcode')
    #描述
    #column_descriptions = {'missionid':'任务ID', 'barcode':'资产标签号'}
    #字段显示名称
    column_labels = {'missionid': '任务ID', 'barcode': '资产标签号'}
    #搜索字段
    column_searchable_list = [mission_barcode.barcode]
    #默认排序字段
    column_default_sort = ('barcode', True)
    #列表每页数量
    page_size = 10
    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to

        super(MissionBarcode, self).__init__(mission_barcode, session, **kwargs)