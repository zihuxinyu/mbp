# -*- coding: utf8 -*-
import random
import string
from config import POSTS_PER_PAGE, ADMINS
from flask_login import current_user, login_required, logout_user, login_user
from flask.globals import g, request, session, session as gsession
from mbp import lm, app, robot, db
from flask.templating import render_template
from sqlalchemy import and_
from werkzeug.utils import redirect
from flask.helpers import url_for, flash
from mbp.forms import LoginForm
from mbp.models import Staff, Snlist, WechatReceive, WechatUser, BarcodeList,portal_user
from Logic import WechatLogic, BarcodeLogic


@lm.user_loader
def load_user(id):
    return portal_user.query.get(id)


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
        # session['remember_me'] = form.remember_me.data
        #return after_login(form.staffid.data)
        sendlogincode(usercode=form.usercode.data)
        flash('验证码发送成功!')
        return redirect(url_for('loginchk', usercode=form.usercode.data))
    return render_template('login.html',action='login',
                               title='登录',
                               form=form)


@app.route('/loginchk', methods=['GET', 'POST'])
def loginchk(source=None, usercode=None):
    """
    验证绑定码是否匹配
    :param source:
    :param usercode:
    :return:
    """
    from forms import WechatChkCode

    usercode = request.args.get('usercode')
    form = WechatChkCode()
    if form.validate_on_submit():
        code = form.code.data
        if usercode and code:
            x=portal_user.query.filter(and_(portal_user.user_code==usercode,
                                            portal_user.msg==code))

            w = x.first()
            if w:
                after_login(usercode)

            else:
                flash('验证失败,请重试')
                return redirect(url_for('login'))
    return render_template('checkcode.html', action='loginchk', opname='登录系统', form=form, title='请输入验证码')


def after_login(user_code=None):
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
    staff =portal_user.query.filter(portal_user.user_code== user_code).first()
    if not staff:
        flash('登录失败，查无此ID')
        return redirect(url_for('login'))
    flash('登录成功')
    # session["user_code"] = staff.user_code
    # remember_me = False
    # if 'remember_me' in session:
    #     remember_me = session['remember_me']
    #     session.pop('remember_me', None)
    login_user(staff, remember=True)
    return 'ok'


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
    send_email('MSGSEND#15605468613#哈哈哈', 'sd-lcgly@chinaunicom.cn', ['sd-lcgly@chinaunicom.cn'],None,None)
    return "ok"


@robot.handler
def echo(message):
    return '抱歉,未能成功识别此{0},请重试'.format(  message.type)


@robot.image
def echo(message):
    import requests

    r = requests.get('http://127.0.0.1:7000/?url=' + message.img)
    WechatLogic.SaveMessage(message=message,
                            imgcontent=r.text)
    bar = BarcodeLogic.GetUnicomBarcode(r.text)
    if bar:
        BarcodeLogic.SaveBarcode(barcodelist=bar, message=message,
                                 type='image')
        return BarcodeLogic.ShowBarDetail(barcodelist=bar,
                                          message=message)
    return r.text


@robot.text
def echo(message, session):
    WechatLogic.SaveMessage(message)
    w = WechatLogic.CheckUser(message.source)
    if not w:
        return WechatLogic.SendBDPage(message)

    #先对输入的文字进行二维码提取.
    bar = BarcodeLogic.GetUnicomBarcode(message.content)
    if bar:
        BarcodeLogic.SaveBarcode(barcodelist=bar, message=message,
                                 type='input')
        return BarcodeLogic.ShowBarDetail(barcodelist=bar,
                                          message=message)

    return message.content


@robot.link
def echo(message, session):
    WechatLogic.SaveMessage(message)
    return  message.url


@robot.location
def echo(message, session):
    WechatLogic.SaveMessage(message)
    return  message.label


@robot.click
def echo(message, session):
    wechat = WechatReceive(id=message.id, target=message.target,
                           source=message.source, time=message.time,
                           raw=message.raw, type=message.type,
                           latitude=message.Latitude, ckey=message.key,
                           longitude=message.Longitude, lprecision=message.Precision
    )
    db.session.add(wechat)
    db.session.commit()
    return str(wechat.guid) + message.key


@robot.voice
def echo(message, session):
    WechatLogic.SaveMessage(message)
    #return  message.media_id
    return  '我听见了.'

@robot.subscribe
def echo(message):
    return "welcome"


@robot.unsubscribe
def echo(message):
    return "dont"


@app.route('/bd/<source>', methods=['GET', 'POST'])
def bd(source=None):
    """
    绑定微信与门户账户
    :param source:
    :return:
    """

    if source:
        w = WechatUser.query.filter(and_(WechatUser.source == source, WechatUser.checked == 1)).first()
        if w:
            return '您已经绑定了' + w.usercode
    from  forms import WechatUserSendcode

    form = WechatUserSendcode()
    if form.validate_on_submit():
        usercode = form.usercode.data.replace('@chinaunicom.cn', '')
        sendcode(source=source, usercode=usercode)
        flash('验证码发送成功!')
        return redirect(url_for('bdchk', usercode=usercode, source=source))
    return render_template('WechatUserSendcode.html',
                           title='绑定',
                           form=form, source=source)


@app.route('/bdchk', methods=['GET', 'POST'])
def bdchk(source=None, usercode=None):
    """
    验证绑定码是否匹配
    :param source:
    :param usercode:
    :return:
    """
    from forms import WechatChkCode

    source = request.args.get('source')
    usercode = request.args.get('usercode')
    form = WechatChkCode()
    if form.validate_on_submit():
        code = form.code.data
        if source and request:
            x = WechatUser.query.filter(and_(WechatUser.source == source,
                                             WechatUser.usercode == usercode,
                                             WechatUser.code == code))

            w = x.first()
            if w:
                x.update({
                    WechatUser.checked: 1
                })

                db.session.commit()
                return render_template('msg.html',msg='绑定成功!请返回微信聊天窗口吧')
    return render_template('checkcode.html',action='bdchk',opname='绑定账户', form=form, title='请输入验证码')


def sendcode(source=None, usercode=None):
    code = WechatLogic.generate_code()
    wechatuser = WechatUser(source=source, usercode=usercode, code=code)
    db.session.add(wechatuser)
    db.session.commit()
    from email import send_email

    send_email('微信绑定验证码是:' + code, 'sd-lcgly@chinaunicom.cn',
               [usercode + '@chinaunicom.cn'], '微信验证码',
               '微信绑定验证码是:' + code)


def sendlogincode(usercode=None):
    code = WechatLogic.generate_code()
    xx=portal_user.query.filter(portal_user.user_code==usercode)
    xx.update({
       portal_user.msg:code
    })
    db.session.commit()
    from email import send_email

    send_email('微信绑定验证码是:' + code, 'sd-lcgly@chinaunicom.cn',
               [usercode + '@chinaunicom.cn'], '微信验证码',
               '微信绑定验证码是:' + code)

@app.route('/showzc/<zcbh>',methods=['GET','POST'])
def showzc(zcbh=None):
    """
    显示资产编号的详细信息
    :param zcbh:
    :return:
    """
    from mbp.models import zczb
    zz=zczb.query.filter(zczb.zcbqh==zcbh).first()
    child=BarcodeLogic.getChild(zcbh)

    return render_template('showzcbq.html',entry=zz,child=child)


@app.route('/test/<source>')
def test(source):
    ww = BarcodeList(source=source, type='input', barcode='sfsdfdsafd')
    db.session.add(ww)
    db.session.commit()
    return str(ww.guid)


@app.route('/cs/<tablename>')
def cs(tablename):
    """
    输入表名,生成MODEL
    :param tablename:
    :return:
    """
    sql="SELECT `COLUMN_NAME`,`DATA_TYPE`,`EXTRA` FROM information_schema.columns WHERE table_schema='DLS' AND table_name='"+ tablename+"'"
    cur= db.engine.execute(sql)
    entries = [dict(COLUMN_NAME=row[0], DATA_TYPE=row[1],EXTRA=row[2]) for row in cur.fetchall()]
    for x in entries:
        print(x)
    return render_template('cs.html',list=entries,tablename=tablename)