# coding: utf-8
from flask.ext.admin import Admin, BaseView, expose
from flask import g
from flask.ext.admin.contrib.sqla import ModelView
from wtforms import SelectField







class MyView(BaseView):
    def is_accessible(self):
        #认证通过的才能显示,可以自定义逻辑
        return g.user.is_authenticated()
    @expose('/')
    def index(self):
        return self.render('admin/index.html')


class MissionBarcode(ModelView):
    form_overrides = dict(missionid=SelectField)
    form_args = dict(
        # Pass the choices to the `SelectField`

        missionid=dict(
            choices=[(0, 'waiting'), (1, 'in_progress'), (2, 'finished')]
        ))
    can_create = True

    # Override displayed fields
    column_list = ('missionid', 'barcode')
    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to
        from mbp.models import mission_barcode
        super(MissionBarcode, self).__init__(mission_barcode, session, **kwargs)