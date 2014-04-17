# -*- coding: utf8 -*-
import StringIO

from dls.config import POSTS_PER_PAGE
from flask_login import current_user, login_required, logout_user, login_user
from flask.globals import g, request, session
from dls import lm, app, db
from flask.templating import render_template
from sqlalchemy import and_
from werkzeug.utils import redirect
from flask.helpers import url_for, flash, make_response
from dls.forms import LoginForm
from dls.models import Staff, Snlist, WechatUser
from Logic import WechatLogic
from Logic.DBLogic import AdoHelper
from dls.Logic.EmailLogic import sendsmscode
from Library.datehelper import now
from Logic.DBLogic import AdoHelper
from  dls.forms import WechatUserSendcode, SearchForm, WechatChkCode


@lm.user_loader
def load_user(id):
    return Staff.query.filter(Staff.staff_id == id).first()


@app.before_request
def before_request():
    g.user = current_user


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    uinfo = Staff.query.filter(Staff.staff_id == g.user.get_id()).first()
    print(uinfo.staff_id)
    return render_template('index.html', uinfo=uinfo)


@app.route('/login', methods=['GET', 'POST'])
def login():
    #    if g.user is not None and g.user.is_authenticated():
    #        return redirect( url_for( 'index' ) )
    form = LoginForm()
    if form.validate_on_submit():
        #session['remember_me'] = form.remember_me.data
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
        if usercode and code and len(code) == 4:
            x = Staff.query.filter(and_(Staff.staff_id == usercode,
                                        Staff.msg == code, Staff.msgexpdate >= now()))

            w = x.first()
            if w:
                staff = Staff.query.filter(Staff.staff_id == usercode).first()
                if not staff:
                    flash('登录失败，查无此ID')
                    return redirect(url_for('login'))

                session["user_code"] = staff.staff_id
                session["chnl_id"] = staff.chnl_id
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
        flash('验证失败，查无此ID')
        return redirect(url_for('index'))
    return render_template('checkcode.html', action='loginchk', opname='登录系统', form=form, title='请输入验证码')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/about')
def about():
    return render_template('about.html')


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
            staff = Staff.query.filter(Staff.staff_id == w.usercode).first()
            login_user(staff, remember=True)
            flash('您已经绑定了' + w.usercode)
            return redirect(url_for('index'))

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

                staff = Staff.query.filter(Staff.staff_id == w.usercode).first()
                session["user_code"] = staff.staff_id
                session["chnl_id"] = staff.chnl_id
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

    sendsmscode(user_code=usercode, code=code)


def sendlogincode(usercode=None):
    code = WechatLogic.generate_code()
    xx = Staff.query.filter(Staff.staff_id == usercode)
    xx.update({
        Staff.msg: code,
        Staff.msgexpdate: now(10)
    })
    db.session.commit()

    sendsmscode(user_code=usercode, code=code)


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
    pass


@app.route('/excel/')
def excel():
    return ""
    import tablib

    type = request.args.get('type')
    if type == 'checked':
        sql = 'SELECT distinct  barcode ,zcbqh,user_code ,swmc,zrbmmc,ztbz,ztbz1,ztbz2,wlwz  ,ggxh,barcodelist.opdate ' \
              '' \
              'FROM zczb, barcodelist WHERE zczb.zcbqh IN(SELECT mission_barcode.barcode  FROM mission_barcode WHERE ' \
              'mission_barcode.missionid = 1 AND mission_barcode.msgid IS NOT NULL) AND barcodelist.barcode = zczb' \
              '.zcbqh order by barcodelist.opdate desc'
        listdata = []
        data = AdoHelper().db().query(sql)
        headers = ([x for x in data[0]])
        for d in data:
            listdata.append([d[x] for x in d])

        data = tablib.Dataset(*listdata, headers=headers)
        output = StringIO.StringIO()
        output.write(data.xls)
        response = make_response(output.getvalue())
        response.headers['Content-Type'] = 'application/vnd.ms-excel'
        response.headers['Content-Disposition'] = 'attachment; filename=list.xls'
        return response


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
@app.route('/showsnlist', methods=['GET', 'POST'])
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

    form = SearchForm()
    if form.validate_on_submit():
        startdate = form.startdate.data
        enddate = form.enddate.data
        t = form.t.data
        return  redirect(url_for('showsnlist',s=startdate,e=enddate,t=t))


    if request.args.get('s') and request.args.get('e'):
        startdate= request.args.get('s')
        enddate= request.args.get('e')
    else:
        startdate = now(-60 * 24 * 30).split(' ')[0]
        enddate = now().split(' ')[0]
        t= request.args.get('t') if request.args.get('t') else 'list'
        return redirect(url_for('showsnlist', s=startdate, e=enddate,t=t))

    sql = "select * from DLS_SNLIST where   open_date <='{1}' and open_date >='{2}' and develop_depart_id  in ( " \
          "select chnl_id from dls_staff_chnl where staff_id='{0}') order by open_date desc"
    sql = sql.format(g.user.get_id(), enddate, startdate)
    #print(sql)
    pagination = AdoHelper().paginate(page, sql=sql, per_page=POSTS_PER_PAGE)

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

    sql="SELECT state_name ,count(serial_number) as count FROM `dls_snlist` where   open_date <='{1}' and open_date >='{2}' and develop_depart_id  in ( " \
        "select chnl_id from dls_staff_chnl where staff_id='{0}') group by state_name order by count desc"
    sql = sql.format(g.user.get_id(), enddate, startdate)
    #print(sql)
    groupdata=AdoHelper().paginate(1,sql=sql,per_page=20000)

    gfields = ['state_name', 'count']
    gfields_cn = ['状态', '数量']
    return render_template('showsnlist.html', pagination=pagination,
                           fields=fields, fields_cn=fields_cn,
                           specfile=specfile, form=form, action='showsnlist',
                           startdate=startdate,enddate=enddate,
                           groupdata=groupdata,gfields=gfields,gfields_cn=gfields_cn)