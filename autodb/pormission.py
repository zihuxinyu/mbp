# coding:utf-8
from functools import wraps
from flask import session, abort
# 定义权限管理类，收集控制器名称。
# 在用户访问中做闭包处理，闭包中通过反射取得正在访问的控制器，并核对用户是否有访问权限
class permission(object):
    def __init__(self, app):
        self.app_name = app.name

    @classmethod  # 类方法，取得控制器列表
    def geturlmap(cls, app):
        '''return a dict'''
        per = {}
        for i in app.url_map._rules:
            if (not i.endpoint.find('static') > -1) and (not i.endpoint.startswith('admin')):
                if per.get(i.endpoint):
                    per[i.endpoint]['rule'].append(i.rule)
                else:
                    per[i.endpoint] = {}
                    per[i.endpoint]['doc'] = app.view_functions[i.endpoint].__doc__
                    per[i.endpoint]['rule'] = [i.rule]
        return per

    @classmethod
    def getpermission(cls, app):
        '''return a set'''
        return set([i.endpoint for i in app.url_map._rules if not i.endpoint == 'static'])

    def check(self, func):  # 检查权限  闭包处理
        @wraps(func)
        def _(*args, **kwargs):
            if session.has_key('logged_in'):  # 判断 session中用户是否登陆。
                usersession = session['logged_in']
            else:
                abort(401)
            func_fullname = self.app_name + '.' + func.__name__  # 取得包名 访问的方法名
            if not usersession:
                abort(401)  # not login
            elif 'Administrator' in usersession.group:  # 如果是管理员
                return func(*args, **kwargs)
            elif not func_fullname in usersession.permission:  #如果 方法名 没有在用户权限中 返回 没有权限
                abort(403)  # no permission
            return func(*args, **kwargs)  # 否则  用户有权限 访问 返回方法调用 。

        return _

    @classmethod
    def login(cls, user):
        #UserSession(user, [i.name for i in user.hasgroups], [i.action for i in user.allpermissions]).updatesession()
        return True

    @classmethod
    def logout(cls):
        session.pop('logged_in', None)
        return True

