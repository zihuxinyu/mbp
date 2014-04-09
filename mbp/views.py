# -*- coding: utf8 -*-
import StringIO
from config import POSTS_PER_PAGE

from flask_login import current_user, login_required, logout_user, login_user
from flask.globals import g, request, session
from mbp import lm, app, robot, db
from flask.templating import render_template
from sqlalchemy import and_, desc
from werkzeug.utils import redirect
from flask.helpers import url_for, flash, make_response
from mbp.forms import LoginForm
from mbp.models import Staff, Snlist, WechatReceive, WechatUser, BarcodeList, portal_user, zczb
from Logic import WechatLogic, BarcodeLogic
from Logic.DBLogic import AdoHelper


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


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    from Logic.MissionLogic import *
    #获取MissionId
    mid = request.args.get('mid')
    mid = '1' if not mid else mid
    remaining = getUnCompletedbyMissionId(mid)
    ended = getCompletedbyMissionId(mid)
    allcount = remaining + ended
    return render_template('index.html', remaining=remaining, ended=ended, allcount=allcount)


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
    from forms import WechatChkCode

    usercode = request.args.get('usercode')
    form = WechatChkCode()
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


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/mission_barcode/<int:page>', methods=['GET', 'POST'])
@app.route('/mission_barcode')
@login_required
def missionbarcode(page=1):
    from models import mission_barcode

    pagination = mission_barcode.query.outerjoin(BarcodeList, mission_barcode.barcode == BarcodeList.barcode).paginate(
        page, POSTS_PER_PAGE, True)
    fields = ['missionid', 'barcode']
    fields_cn = ['任务ID', '资产标签']
    specfile = {'input': '手工输入',
                'image': '拍照上传'}
    return render_template('list.html', pagination=pagination,
                           fields=fields, fields_cn=fields_cn)


@app.route('/list/<int:page>', methods=['GET', 'POST'])
@app.route('/list')
@login_required
def list(page=1):
    """
    展示代理商列表
    :param page:
    :return:
    """
    pagination = Staff.query.filter(Staff.chnl_id.like('%1%')).paginate(page, POSTS_PER_PAGE, True)
    fields = ['staffid', 'chnl_id', 'chnl_name']
    fields_cn = ['登录ID', '代理商ID', '代理商名称']
    specfile = {}
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


@robot.handler
def echo(message):
    return '抱歉,未能成功识别此{0},请重试'.format(message.type)


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
    return message.url


@robot.location
def echo(message, session):
    WechatLogic.SaveMessage(message)
    return message.label


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
    return '我听见了.'


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
            staff = portal_user.query.filter(portal_user.user_code == w.usercode).first()
            login_user(staff, remember=True)
            flash('您已经绑定了' + w.usercode)
            return redirect(url_for('index'))

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

                staff = portal_user.query.filter(portal_user.user_code == w.usercode).first()
                login_user(staff, remember=True)
                db.session.commit()
                flash('绑定成功')
                return redirect(url_for('index'))

    return render_template('checkcode.html', action='bdchk', opname='绑定账户', form=form, title='请输入验证码')


def sendcode(source=None, usercode=None):
    code = WechatLogic.generate_code()
    wechatuser = WechatUser(source=source, usercode=usercode, code=code)
    db.session.add(wechatuser)
    db.session.commit()
    from email import sendsmscode

    sendsmscode(user_code=usercode, code=code)


def sendlogincode(usercode=None):
    code = WechatLogic.generate_code()
    xx = portal_user.query.filter(portal_user.user_code == usercode)
    xx.update({
        portal_user.msg: code
    })
    db.session.commit()
    from email import sendsmscode

    sendsmscode(user_code=usercode, code=code)


@app.route('/showzc/', methods=['GET', 'POST'])
@login_required
def showzc(zcbh=None):
    """
    显示资产编号的详细信息
    :param zcbh:
    :return:
    """

    from mbp.models import zczb
    from  forms import BarcodeListUpdate

    if (not zcbh ) and request.args.get('zcbh'):
        zcbh = str(request.args.get('zcbh'))
    msgid = request.args.get('msgid')

    bb = BarcodeList.query.filter(and_(BarcodeList.user_code == g.user.user_code),
                                  BarcodeList.barcode == zcbh
    )
    form = BarcodeListUpdate()
    # 下电标识:
    # 报废标识:未报废, 闲置-待报废, 已报废
    # 设备生命周期:在用-长期使用, 在用-两年内下线（2015年内）, 在用-年内下线（2014年内）, 闲置-可用, 不可用, 在用-开发测试

    form.ztbz.choices = [('未下电', '未下电'), ('已下电-已拆除', '已下电-已拆除'), ('已下电-待拆除', '已下电-待拆除')]
    form.ztbz1.choices = [('未报废', '未报废'), ('闲置-待报废', '闲置-待报废'), ('已报废', '已报废')]
    form.ztbz2.choices = [('在用-长期使用', '在用-长期使用'), ('在用-两年内下线（2015年内）', '在用-两年内下线（2015年内）'),
                          ('闲置-可用', '闲置-可用'), ('在用-开发测试', '在用-开发测试')]
    if form.validate_on_submit():
        #更新最新状态
        ztbz = form.ztbz.data
        ztbz1 = form.ztbz1.data
        ztbz2 = form.ztbz2.data
        wlwz = form.wlwz.data
        if bb:
            bb.update({BarcodeList.ztbz1: ztbz1, BarcodeList.ztbz2: ztbz2,
                       BarcodeList.ztbz: ztbz, BarcodeList.wlwz: wlwz})

            db.session.commit()
        flash('更新成功')

    zz = zczb.query.filter(zczb.zcbqh == zcbh).first()
    child = BarcodeLogic.getChild(zcbh)

    return render_template('showzcbq.html', form=form, entry=zz, child=child, barcodeinfo=bb.first())


@app.route('/barcodelist/<int:page>', methods=['GET', 'POST'])
@app.route('/barcodelist')
@login_required
def barcodelist(page=1):
    """
    清查日志
    :param page:
    :return:
    """
    sql = "SELECT *  FROM `barcodelist` ORDER BY `barcodelist`.`opdate` DESC"

    #sql="select * from zczb"
    xx = AdoHelper().paginate(page, sql=sql)
    #pagination = BarcodeList.query.order_by(desc(BarcodeList.opdate)).distinct(BarcodeList.barcode).paginate(page,POSTS_PER_PAGE, True)
    fields = ['barcode', 'ztbz', 'ztbz1', 'ztbz2', 'wlwz', 'user_code', 'topdpt', 'type', 'opdate']
    fields_cn = ['二维码', '下电标识', '报废标识', '生命周期', '物理位置', '账户', '部门', '类型', '时间']

    specfile = {'input': '手工输入',
                'image': '拍照上传',
                'None': ''}
    return render_template('list.html', pagination=xx,
                           fields=fields, fields_cn=fields_cn, specfile=specfile)


@app.route('/unchecked/<int:page>', methods=['GET', 'POST'])
@app.route('/unchecked/', methods=['GET', 'POST'])
@login_required
def unchecked(page=1):
    """
    没有核查的资产列表
    :param page:
    :return:
    """
    #获取MissionId
    mid = request.args.get('mid')
    mid = '1' if not mid else mid

    from Logic import MissionLogic

    zz = zczb.query.filter(zczb.zcbqh.in_(
        MissionLogic.getUnCompleteZCBQHbyMissionId(mid)
    ))
    pagination = zz.paginate(page, POSTS_PER_PAGE, True)
    fields = ['zcbqh', 'swmc', 'ggxh', 'zrbmmc']
    fields_cn = ['资产标签号', '实物名称', '规格型号', '责任部门名称']
    specfile = {'input': '手工输入',
                'image': '拍照上传'}
    return render_template('list.html', pagination=pagination,
                           fields=fields, fields_cn=fields_cn, specfile=specfile)


@app.route('/checked/<int:page>', methods=['GET', 'POST'])
@app.route('/checked/', methods=['GET', 'POST'])
@login_required
def checked(page=1):
    """
    已经核查的资产列表
    :param page:
    :return:
    """
    #获取MissionId
    mid = request.args.get('mid')
    mid = '1' if not mid else mid

    from Logic import MissionLogic

    sql = 'SELECT distinct  barcode ,zcbqh,user_code ,swmc,zrbmmc,ztbz,ztbz1,ztbz2,wlwz  ,ggxh,barcodelist.opdate ' \
          'FROM zczb, ' \
          'barcodelist WHERE zczb.zcbqh IN(SELECT mission_barcode.barcode  FROM mission_barcode WHERE mission_barcode' \
          '.missionid = {0} AND mission_barcode.msgid IS NOT NULL) AND barcodelist.barcode = zczb.zcbqh order by ' \
          'barcodelist.opdate desc '

    sql = sql.format(MissionLogic.getCompleteZCBQHbyMissionId(mid))
    print(sql)
    xx = AdoHelper().paginate(page, sql=sql)
    fields = ['zcbqh', 'swmc', 'ggxh', 'ztbz', 'ztbz1', 'ztbz2', 'wlwz', 'user_code', 'zrbmmc', 'opdate']
    fields_cn = ['资产标签号', '实物名称', '规格型号', '下电标识', '报废标识', '生命周期', '物理位置', '核查人', '责任部门名称', '操作时间']
    specfile = {'None': '12'}
    #各列的格式化处理
    formater={'zcbqh':'<a href=/showzc/?zcbh={0}>{0}</a>'}
    return render_template('yicha.html', pagination=xx, formater=formater,
                           fields=fields, fields_cn=fields_cn, specfile=specfile)


@app.route('/cs/<tablename>')
def cs(tablename):
    """
    输入表名,生成MODEL
    :param tablename:
    :return:
    """
    sql = "SELECT `COLUMN_NAME`,`DATA_TYPE`,`EXTRA` FROM information_schema.columns WHERE table_schema='DLS' AND " \
          "table_name='" + tablename + "'"
    cur = db.engine.execute(sql)
    entries = [dict(COLUMN_NAME=row[0], DATA_TYPE=row[1], EXTRA=row[2]) for row in cur.fetchall()]
    for x in entries:
        print(x)
    return render_template('cs.html', list=entries, tablename=tablename)




@app.route('/test/<int:page>/')
@app.route('/test/')
def test(page=1):
    sql = 'SELECT zczb.*,barcodelist.ztbz FROM zczb , barcodelist  WHERE zczb.zcbqh IN(SELECT mission_barcode.barcode ' \
          'AS mission_barcode_barcode FROM mission_barcode WHERE mission_barcode.missionid = 1 AND mission_barcode' \
          '.msgid IS NOT NULL) AND barcodelist.barcode = zczb.zcbqh'
    #sql="select * from zczb"
    xx = AdoHelper().paginate(page, sql=sql)
    fields = ['zcbqh', 'ztbz', 'swmc', 'ggxh', 'zrbmmc']
    fields_cn = ['资产标签号', '状态标识', '实物名称', '规格型号', '责任部门名称']
    specfile = {'未下电': '手工输入',
                'image': '拍照上传', 'None': ''}
    return render_template('list.html', pagination=xx,
                           fields=fields, fields_cn=fields_cn, specfile=specfile)


@app.route('/excel/')
def excel():

    import tablib

    type = request.args.get('type')
    if type=='checked':
        sql='SELECT distinct  barcode ,zcbqh,user_code ,swmc,zrbmmc,ztbz,ztbz1,ztbz2,wlwz  ,ggxh,barcodelist.opdate FROM zczb, barcodelist WHERE zczb.zcbqh IN(SELECT mission_barcode.barcode  FROM mission_barcode WHERE mission_barcode.missionid = 1 AND mission_barcode.msgid IS NOT NULL) AND barcodelist.barcode = zczb.zcbqh order by barcodelist.opdate desc'
        pass

    headers = ('area', 'user', 'recharge')
    data = [
        ('1', 'Rooney', 20),
        ('2', 'John', 30),
    ]
    data = tablib.Dataset(*data, headers=headers)
    

    output = StringIO.StringIO()
    output.write(data.xls)
    response = make_response(output.getvalue())
    response.headers['Content-Type'] = 'application/vnd.ms-excel'
    response.headers['Content-Disposition'] = 'attachment; filename=123.xls'
    return response

