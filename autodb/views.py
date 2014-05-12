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
    return "dfsads"


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

    return usercode+pwd


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))





@app.route('/sqladd/', methods=['GET', 'POST'])
@login_required
def sqladd():
    """
    sql列表

    :return:
    """
    from autodb.models import sqllist
    from  forms import FMsqllist
    from Library.datehelper import now

    form = FMsqllist()
    form.frequency.choices = [('hour:2', '每2小时'), ('已下电-已拆除', '已下电-已拆除')]
    if form.validate_on_submit():
        #更新最新状态
        title = form.title.data
        sqlContent = form.sqlContent.data
        paras = form.paras.data
        frequency = form.frequency.data

        user_code = form.user_code.data
        opdate = now()
        msqllist = sqllist(title=title, sqlContent=sqlContent, paras=paras, frequency=frequency,
                           user_code=user_code, opdate=opdate)
        db.session.add(msqllist)
        db.session.commit()
        flash('添加成功')

    return render_template('showsqllist.html', form=form, action='sqllist')

