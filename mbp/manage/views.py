# coding: utf-8
from flask.ext.admin import Admin, BaseView, expose
from flask import g
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.admin.form import rules
from markupsafe import Markup
from sqlalchemy.event import listens_for
from wtforms import SelectField
from mbp.models import mission_barcode,mission_user,mission,usergroup,BaseAuth
from mbp.Logic.MissionLogic import getMissions,getMissionNameById

def _getMissionHref(view, context, model, name):
    return Markup("<a href='/index?mid={0}' target=_blank>{0}-{1}</a>".format(model.missionid,getMissionNameById(model.missionid)))



def _getUsergroupName(view, context, model, name):
    groupname={'1':'系统管理员','2':'普通用户'}
    return Markup("{0}".format(groupname[model.groupid]))


class MyView(BaseView):
    def is_accessible(self):
        #认证通过的才能显示,可以自定义逻辑
        return g.user.is_authenticated()
    @expose('/')
    def index(self):
        return self.render('admin/index.html')


class Mission(BaseAuth,ModelView):

    #edit_template = 'admin/edit.html'


    #可以创建新的
    can_create = False
    can_delete = False

    #显示字段
    column_list = ( 'missionname','startdate','enddate')
    #设置过滤器
    column_filters = ('missionname',)
    #描述
    #column_descriptions = {'missionid':'任务ID', 'barcode':'资产标签号'}
    #字段显示名称
    column_labels = {'missionname': '任务名称', 'startdate': '开始时间','enddate':'结束时间'}
    #搜索字段
    column_searchable_list = [mission.missionname]
    #默认排序字段
    column_default_sort = ('missionname', True)
    #列表每页数量
    page_size = 10

    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to

        super(Mission, self).__init__(mission, session, **kwargs)

class MissionBarcode(BaseAuth,ModelView):

    #edit_template = 'admin/edit.html'
    form_overrides = dict(missionid=SelectField)
    form_args = dict(
        # Pass the choices to the `SelectField`

        missionid=dict(
            choices=getMissions()
        ))



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


class MissionUser(BaseAuth,ModelView):
    #edit_template = 'admin/edit.html'
    form_overrides = dict(missionid=SelectField)
    form_args = dict(
        # Pass the choices to the `SelectField`

        missionid=dict(
            choices=getMissions()
        ))

    # form_create_rules = [
    #     rules.Header("dsdsdsd"),
    #     rules.HTML('''
    #     <font color=red>ddd</font>
    #     '''),
    #
    #     rules.FieldSet(('missionid', 'barcode'), '任务信息'),
    #
    # ]

    column_formatters = {
        'missionid': _getMissionHref
    }
    #可以创建新的
    can_create = True

    #显示字段
    column_list = ('missionid', 'user_code')
    #设置过滤器
    column_filters = ('missionid', 'user_code')
    #描述
    #column_descriptions = {'missionid':'任务ID', 'user_code':'4A工号'}
    #字段显示名称
    column_labels = {'missionid': '任务ID', 'user_code': '4A工号'}
    #搜索字段
    column_searchable_list = [mission_user.user_code]
    #默认排序字段
    column_default_sort = ('user_code', True)
    #列表每页数量
    page_size = 10

    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to

        super(MissionUser, self).__init__(mission_user, session, **kwargs)


class UserGroup(BaseAuth,ModelView):
    #edit_template = 'admin/edit.html'
    form_overrides = dict(groupid=SelectField)
    form_args = dict(
        # Pass the choices to the `SelectField`

        groupid=dict(
            choices=[('1','系统管理员'),('2','普通用户')]
        ))

    # form_create_rules = [
    #     rules.Header("dsdsdsd"),
    #     rules.HTML('''
    #     <font color=red>ddd</font>
    #     '''),
    #
    #     rules.FieldSet(('missionid', 'barcode'), '任务信息'),
    #
    # ]

    column_formatters = {
        'groupid': _getUsergroupName
    }
    #可以创建新的
    can_create = True

    #显示字段
    column_list = ('groupid', 'user_code')
    #设置过滤器
    column_filters = ('groupid', 'user_code')
    #描述
    #column_descriptions = {'missionid':'任务ID', 'user_code':'4A工号'}
    #字段显示名称
    column_labels = {'groupid': '角色ID', 'user_code': '4A工号'}
    #搜索字段
    column_searchable_list = [usergroup.user_code]
    #默认排序字段
    column_default_sort = ('user_code', True)
    #列表每页数量
    page_size = 10

    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to

        super(UserGroup, self).__init__(usergroup, session, **kwargs)