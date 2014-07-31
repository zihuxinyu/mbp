# coding: utf-8
'''
文件作用:user相关操作
'''
from flask_login import logout_user, login_user
from werkzeug.utils import redirect
from flask.helpers import url_for, flash
from flask import Blueprint,g
from flask.globals import request, session
from flask.templating import render_template
from autodb.models.portal import portal_user
import requests
from pony.orm import *
user = Blueprint("user", __name__)


@user.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


@user.route('/loginchk/', methods=['GET', 'POST'])
def loginchk():
    data = (request.form.get("submitData"))
    import json
    data = json.loads(data)
    usercode = data['username']
    pwd = data['pwd']
    url = "http://134.44.36.127:8080/sso/default.aspx?name={0}&psw={1}"

    r = requests.get(url.format(usercode, pwd))
    if r.text:


        with db_session:
            staff = select(p for p in portal_user if p.user_code == usercode).first()
            if not staff:
                flash('登录失败，查无此ID')
                return "登录失败，查无此ID"
            remember_me = False
            if 'remember_me' in session:
                remember_me = session['remember_me']
                session.pop('remember_me', None)
            from autodb.models.portal import users
            lu=users(staff.user_code)

            login_user(lu, remember=True)
            g.user=lu
            return "登录成功"
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
        remember_me = False
        if 'remember_me' in session:
            remember_me = session['remember_me']
            session.pop('remember_me', None)
        from autodb.models.portal import users

        lu = users(staff.user_code)
        login_user(lu, remember=True)
    return ""