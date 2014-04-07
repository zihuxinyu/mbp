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


@lm.user_loader
def load_user(id):
    return portal_user.query.filter(portal_user.user_code == id).first()


@app.before_request
def before_request():
    g.user = current_user


@app.errorhandler(500)
def internal_error(error):
    #db.session.rollback()
    return render_template('500.html'), 500


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



@app.route('/', methods=['GET', 'POST'])
@app.route('/sqllist/', methods=['GET', 'POST'])
@login_required
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
