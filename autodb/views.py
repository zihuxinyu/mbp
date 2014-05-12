# -*- coding: utf8 -*-
from autodb.Logic.LoginLogic import sendlogincode
from autodb.models import portal_user

from flask_login import current_user, login_required, logout_user, login_user
from flask.globals import g, request, session
from autodb import app,db,lm
from flask.templating import render_template
from sqlalchemy.sql.elements import and_
from werkzeug.utils import redirect
from flask.helpers import url_for, flash
from autodb.forms import LoginForm


@app.route('/cs/<tablename>')
def cs(tablename):
    """
    输入表名,生成MODEL
    :param tablename:
    :return:
    """
    from config import DB_DATEBASE

    sql = "SELECT `COLUMN_NAME`,`DATA_TYPE`,`EXTRA`,`COLUMN_COMMENT` FROM information_schema.columns WHERE table_schema='{0}' AND " \
          "table_name='{1}'".format(DB_DATEBASE, tablename)
    cur = db.engine.execute(sql)
    entries = [dict(COLUMN_NAME=row[0], DATA_TYPE=row[1], EXTRA=row[2], COLUMN_COMMENT=row[3]) for row in cur.fetchall()]

    return render_template('cs.html', list=entries, tablename=tablename)


@lm.user_loader
def load_user(id):
    return portal_user.query.filter(portal_user.user_code == id).first()


@app.before_request
def before_request():
    g.user = current_user


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


@app.route('/loginchk/', methods=['GET', 'POST'])
def loginchk():
    data=(request.form.get("submitData"))
    import json

    data = json.loads(data)
    usercode= data['username']
    pwd= data['pwd']
    url="http://134.44.36.127:8080/sso/default.aspx?name={0}&psw={1}"
    import requests
    r=requests.get(url.format(usercode,pwd))
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


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
