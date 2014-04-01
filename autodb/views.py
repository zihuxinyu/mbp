# -*- coding: utf8 -*-

from flask_login import current_user, login_required, logout_user, login_user
from flask.globals import g, request, session
from autodb import app,db
from flask.templating import render_template
from werkzeug.utils import redirect
from flask.helpers import url_for, flash
from autodb.forms import LoginForm



@app.before_request
def before_request():
    g.user = current_user


@app.errorhandler(500)
def internal_error(error):
    #db.session.rollback()
    return render_template('500.html'), 500


@app.route('/index', methods=['GET', 'POST'])
def index():
    return "index"


@app.route('/login', methods=['GET', 'POST'])
def login():

    return "login"


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/', methods=['GET', 'POST'])
@app.route('/sqllist/', methods=['GET', 'POST'])
def sqllist():
    """
    sql列表

    :return:
    """
    from autodb.models import sqllist
    from  forms import FMsqllist
    from Logic import DateLogic

    form = FMsqllist()
    form.frequency.choices = [('hour:2', '每2小时'), ('已下电-已拆除', '已下电-已拆除')]
    if form.validate_on_submit():
        #更新最新状态
        title = form.title.data
        sqlContent = form.sqlContent.data
        paras = form.paras.data
        frequency = form.frequency.data

        user_code = form.user_code.data
        opdate = DateLogic.now()
        msqllist = sqllist(title=title, sqlContent=sqlContent, paras=paras, frequency=frequency,
                           user_code=user_code, opdate=opdate)
        db.session.add(msqllist)
        db.session.commit()
        flash('添加成功')

    return render_template('showsqllist.html', form=form, action='sqllist')
