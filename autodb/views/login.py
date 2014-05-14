# coding: utf-8
'''
文件作用:user相关操作
'''
from flask_login import logout_user, login_user
from werkzeug.utils import redirect
from flask.helpers import url_for, flash
from flask import Blueprint
from flask.globals import request, session
from flask.templating import render_template
from autodb.modelx import portal_user
import requests
from flask import jsonify
user = Blueprint("user", __name__
)


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
        staff = portal_user.query.filter(portal_user.user_code == usercode).first()
        if not staff:
            flash('登录失败，查无此ID')
            return "登录失败，查无此ID"

        remember_me = False
        if 'remember_me' in session:
            remember_me = session['remember_me']
            session.pop('remember_me', None)
        login_user(staff, remember=True)

        return "登录成功"
    return "登录失败"


@user.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
