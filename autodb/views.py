# -*- coding: utf8 -*-
from Library.jsonhelper import CJsonEncoder
from autodb.Logic.DBLogic import AdoHelper
from autodb.Logic.LoginLogic import sendlogincode
from autodb.config import POSTS_PER_PAGE
from autodb.models import portal_user

from Library.minihelper import getData
from Library.minihelper import getData
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




@app.route('/index', methods=['GET', 'POST'])
def index():
    return redirect(url_for('sqllist'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    #    if g.user is not None and g.user.is_authenticated():
    #        return redirect( url_for( 'index' ) )
    form = LoginForm()
    if form.validate_on_submit():
        # session['remember_me'] = form.remember_me.data
        #return after_login(form.staffid.data)
        sendlogincode(usercode=form.usercode.data)
        flash('验证码发送成功!')
        return redirect(url_for('loginchk', usercode=form.usercode.data))
    return render_template('login.html', action='login',
                           title='登录', opname='登录系统',
                           form=form)


@app.route('/loginchk', methods=['GET', 'POST'])
def loginchk(source=None, usercode=None):
    """
    验证绑定码是否匹配
    :param source:
    :param usercode:
    :return:
    """
    from forms import LoginChkCode

    usercode = request.args.get('usercode')
    form = LoginChkCode()
    if form.validate_on_submit():
        code = form.code.data
        if usercode and code:
            x = portal_user.query.filter(and_(portal_user.user_code == usercode,
                                              portal_user.msg == code))

            w = x.first()
            if w:
                staff = portal_user.query.filter(portal_user.user_code == usercode).first()
                if not staff:
                    flash('登录失败，查无此ID')
                    return redirect(url_for('login'))

                session["user_code"] = staff.user_code
                remember_me = False
                if 'remember_me' in session:
                    remember_me = session['remember_me']
                    session.pop('remember_me', None)
                login_user(staff, remember=True)
                flash('登录成功')
                return redirect(url_for('index'))

            else:
                flash('验证失败,请重试')
                return redirect(url_for('login'))
    return render_template('checkcode.html', action='loginchk', opname='登录系统', form=form, title='请输入验证码')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/sqllistdata/', methods=['GET', 'POST'])
def sqllistdata():
    '''
    获取sqllist数据
    pageIndex	0
pageSize	10
sortField	createtime
sortOrder	desc
    '''

    pageIndex = int(request.form["pageIndex"]) if request.form["pageIndex"] else 0;
    pageSize = int(request.form["pageSize"]) if request.form["pageSize"] else 3;

    sql = "select * from sqllist";
    sqlwhere = " 1";

    return getData(sql, sqlwhere, pageSize, pageIndex, AdoHelper().db())



@app.route('/sqlresult/', methods=['GET', 'POST'])
def sqlresult():
    '''
    获取sqlresult数据
    '''

    pageIndex = int(request.form["pageIndex"]) if request.form["pageIndex"] else 0;
    pageSize = int(request.form["pageSize"]) if request.form["pageSize"] else 3;
    sguid= request.form["sguid"]

    sql = "select * from sqlresult";
    if sguid:
        sqlwhere = " sguid='{0}' order by guid desc".format(sguid);

        return getData(sql, sqlwhere, pageSize, pageIndex, AdoHelper().db())


@app.route('/sqllist/', methods=['GET', 'POST'])
@app.route('/sqllist/<int:page>', methods=['GET', 'POST'])
def sqllist(page=1):
    """
    sql列表

    :return:
    """



    return render_template('sqllist.html')



@app.route('/', methods=['GET', 'POST'])
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
