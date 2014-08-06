# coding: utf-8
'''
文件作用:user相关操作
'''
from autodb.Logic.PermissionLogic import getMenusByUser_code,getGroupidByUsercode,getModulenameByGroupId
from flask_login import logout_user, login_user
from werkzeug.utils import redirect
from flask.helpers import url_for
from flask import Blueprint,g
from flask.globals import request, session
from flask.templating import render_template
from autodb.models.portal import portal_user
import requests
from Library.flaskhelper import getargs2json
from pony.orm import *
user = Blueprint("user", __name__)


@user.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


@user.route('/loginchk/', methods=['GET', 'POST'])
def loginchk():

    data = getargs2json('submitData')
    usercode = data['username']
    pwd = data['pwd']
    url = "http://134.44.36.127:8080/sso/default.aspx?name={0}&psw={1}"

    r = requests.get(url.format(usercode, pwd))
    if r.text:
        sso(usercode)
    return "登录失败"


@user.route('/logout')
def logout():
    logout_user()
    session['username']=None
    return redirect(url_for('root.index'))


@user.route('/sso/<string:usercode>')
def sso(usercode):
    with db_session:
        staff = select(p for p in portal_user if p.user_code == usercode).first()
        if not staff:
            return "登录失败，查无此ID"

        from autodb.models.portal import users


        lu = users(staff.user_code)
        login_user(lu, remember=True)


        # 保存用户菜单
        session['menu'] = getMenusByUser_code(g.user.get_id())
        #保存用户角色
        session['groupid']=getGroupidByUsercode(g.user.get_id())
        #保存用户模块
        session['groupname']=getModulenameByGroupId(session['groupid'])
    return "success"