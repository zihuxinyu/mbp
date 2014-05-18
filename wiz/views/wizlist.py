# coding: utf-8
from Library import flaskhelper
from Library.flaskhelper import getargs,getargs2json
from Library.minihelper import getGridData,saveData
from flask import Blueprint
from flask.ext.login import login_required
from flask.templating import render_template
from pony.orm import *
from wiz.models.wiz_user import wiz_user
from wiz.models.invite_list import invite_list
from wiz.models.wiz_sell import wiz_sell
from wiz.Logic.wizlogic import startmain
import json

wizlist = Blueprint("wizlist", __name__)


@wizlist.route('/wizlistdata/', methods=['GET', 'POST'])
@db_session
@login_required
def wizlistdata():
    pageIndex = int(getargs("pageIndex", 0))
    pageSize = int(getargs("pageSize", 0))

    total = select(count(p.guid) for p in invite_list).first()
    data = select(p for p in invite_list).order_by(desc(invite_list.opdate)).limit(pageSize, pageSize * pageIndex)
    return getGridData(invite_list, total, data)


@wizlist.route('/wizdata/', methods=['GET', 'POST'])
@db_session
@login_required
def wizdata():
    invite_code=flaskhelper.getargs('invite_code')
    total =1
    data = select(p for p in wiz_user if p.regcode== invite_code)
    return getGridData(wiz_user, total, data)

@wizlist.route('/wizresult/', methods=['GET', 'POST'])
@db_session
@login_required
def wizresult():
    '''
    获取sqlresult数据
    '''

    pageIndex = int(getargs("pageIndex", 0))
    pageSize = int(getargs("pageSize", 0))
    invite_code = getargs("invite_code")

    total = select(count(p.guid) for p in wiz_user if p.invite_code == invite_code).first()
    data = select(p for p in wiz_user if p.invite_code == invite_code).order_by(desc(wiz_user.opdate)).limit(pageSize,
                                                                                                             pageSize
                                                                                                             *
                                                                                                             pageIndex)
    return getGridData(wiz_user, total, data)


@wizlist.route('/wizstart/', methods=['GET', 'POST'])
def wizstart():
    '''
    开始
    '''
    invite_code = getargs("invite_code")
    counts = getargs("counts")
    if invite_code and count:
        startmain(invite_code, counts)
        return "请稍后"
    else:
        return "输入有误"


@wizlist.route('/list/', methods=['GET', 'POST'])
@login_required
def list(page=1):
    """
    sql列表

    :return:
    """

    return render_template('wizlist.html')


@wizlist.route('/saveinvite/', methods=['GET', 'POST'])
@login_required
@db_session
def saveinvite():
    data = flaskhelper.getargs2json("data")
    saveData(invite_list,data)
    return "ok"


@wizlist.route('/caiji/<int:askcount>')
@wizlist.route('/caiji/')
def caiji(askcount=100):
    from wiz.Logic.Mysqldb import db
    '''
    采集小账户到待刷列表
    type 1 定制
         2 自动
    askcount : 初始积分兑换次数
    '''

    sql='''
    insert into invite_list (invite_code,askcount,realcount,type,opdate)
select w.regcode ,'{0}' as askcount ,'0' as realcount ,'2' as type ,now() as opdate from wiz_user w where w.regcode
not in (select distinct invite_code from invite_list)
        '''
    with db_session:
        db.execute(sql.format(askcount))
    return "ok"

@wizlist.route('/autostart/')
@db_session
def autostart():
    '''
    定时自动开始赠送积分
    '''

    dlist=select(  (p.invite_code,p.askcount-p.realcount) for p in invite_list if (p.askcount-p.realcount)>0).limit(10)
    for l in dlist:
        startmain(str(l[0]),l[1])
    return "ok"

@wizlist.route('/sell/',methods=['POST'])
@db_session
def sell():
    '''
    销售
    '''
    data = flaskhelper.getargs2json("data")
    price = flaskhelper.getargs('price')

    for item in data:
        invite_code = item['invite_code']
        il=select(p for p in invite_list if p.invite_code==invite_code).first()
        wu=select(p for p in wiz_user if p.regcode==invite_code).first()
        wiz_sell(invite_code=invite_code,price=price,realcount=il.realcount,reguser=wu.reguser,regpsw=wu.regpsw)
        il.delete()
        wu.delete()
    return "ok"