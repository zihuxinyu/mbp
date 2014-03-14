# -*- coding: utf8 -*-
import random
from config import POSTS_PER_PAGE, ADMINS
from flask_login import current_user, login_required, logout_user, login_user
from flask.globals import g, request, session
from mbp import lm, app, robot
from flask.templating import render_template
from werkzeug.utils import redirect
from flask.helpers import url_for, flash
from mbp.forms import LoginForm
from mbp.models import Staff, Snlist


@lm.user_loader
def load_user(id):
    return Staff.query.get(id)


@app.before_request
def before_request():
    g.user = current_user


@app.errorhandler(500)
def internal_error(error):
    #db.session.rollback()
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    #    if g.user is not None and g.user.is_authenticated():
    #        return redirect( url_for( 'index' ) )
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        return after_login(form.staffid.data)
    return render_template('login.html',
                           title='Sign In',
                           form=form)


def after_login(staffid=None):
    #    if resp.email is None or resp.email == "":
    #        flash( '登录失败' )
    #        return redirect( url_for( 'login' ) )
    # user = User.query.filter_by( email = resp.email ).first()

    #        nickname = resp.nickname
    #        if nickname is None or nickname == "":
    #            nickname = resp.email.split( '@' )[0]
    #        nickname = User.make_valid_nickname( nickname )
    #        nickname = User.make_unique_nickname( nickname )
    #        user = User( nickname = nickname, email = resp.email, role = ROLE_USER )
    #        db.session.add( user )
    #        db.session.commit()
    #        # make the user follow him/herself
    #        db.session.add( user.follow( user ) )
    #        db.session.commit()
    staff = Staff.query.get(staffid)
    if not staff:
        flash('登录失败，查无此ID')
        return redirect(url_for('login'))
    flash('登录成功')
    session["chnl_id"] = staff.chnl_id
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(staff, remember=remember_me)
    return redirect(request.args.get('next') or url_for('showsnlist'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/list/<int:page>', methods=['GET', 'POST'])
@app.route('/list')
@login_required
def list(page=1):
    """
玩儿玩儿
    :param page:
    :return:
    """
    pagination = Staff.query.filter(Staff.chnl_id.like('%1%')).paginate(page, POSTS_PER_PAGE, True)
    fields = ['staffid', 'chnl_id', 'chnl_name']
    fields_cn = ['登录ID', '代理商ID', '代理商名称']
    specfile = {'sdsc-yhjzl1': '<span class="label label-danger">停机</span>',
                '1': 'dddddddd'}
    return render_template('list.html', pagination=pagination,
                           fields=fields, fields_cn=fields_cn,
                           specfile=specfile)


@app.route('/showsnlist/<int:page>', methods=['GET', 'POST'])
@app.route('/showsnlist')
@login_required
def showsnlist(page=1):
    """
开通
申请停机
挂失停机
局方停机
欠费停机
申请销号
高额停机
欠费销号
申请预销停机
    :param page:
    :return:
    """

    pagination = Snlist.query.filter(Snlist.develop_depart_id == session["chnl_id"]).order_by(
        Snlist.serial_number.desc()).paginate(page, POSTS_PER_PAGE,
                                              True)
    fields = ['serial_number', 'open_date', 'user_state_codeset']
    fields_cn = ['号码', '开户时间', '状态']
    specfile = {'0': '<span class="label label-success">开通</span>',
                '1': '<span class="label label-warning">申请停机</span>',
                '2': '<span class="label label-warning">挂失停机</span>',
                '4': '<span class="label label-warning">局方停机</span>',
                '5': '<span class="label label-warning">欠费停机</span>',
                '6': '<span class="label label-info">申请销号</span>',
                '7': '<span class="label label-warning">高额停机</span>',
                '9': '<span class="label label-danger">欠费销号</span>',
                'F': '<span class="label label-danger">申请预销停机</span>'
    }
    return render_template('list.html', pagination=pagination,
                           fields=fields, fields_cn=fields_cn,
                           specfile=specfile)


@app.route('/sendmail')
def sendtest():
    from email import send_email

    send_email('ss', 'aixinit@126.com', ['aixinit@126.com'], 'textboy', 'htmlbody')
    return "ok"


@app.route('/wizapp/<user_code>/')
@app.route('/wizapp/<user_code>/')
def wizapp(user_code=None):
    from models import wiz_user

    user_code = user_code.encode('utf8')

    list = wiz_user.query.filter(wiz_user.invite_code == user_code).count()
    return render_template('listwiz.html',allcount=list)


@app.route('/wizstart/', methods=['GET', 'POST'])
def wizstart():
    from  wiz import startmain
    from forms import WizStartForm
    form = WizStartForm()
    if form.validate_on_submit():
        usercode=form.usercode.data
        counts=form.counts.data
        startmain(usercode,counts)
        return redirect(url_for('wizapp', user_code=usercode))
    return render_template('wizstart.html',
                           title='start',
                           form=form)


@robot.handler
def echo(message):
    return 'Hello World'


@robot.image
def echo(message):
    import  requests
    r=requests.get('http://127.0.0.1:7000/?url='+message.img)
    return r.text

