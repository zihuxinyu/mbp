# coding: utf-8
from Library import flaskhelper
from Library.flaskhelper import getargs
from Library.minihelper import getGridData,Row
from flask import Blueprint
from flask.ext.login import login_required
from flask.templating import render_template
from pony.orm import *
from wiz.models.wiz_user import wiz_user
from wiz.models.invite_list import invite_list
from wiz.Logic.wizlogic import startmain

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
def saveinvite():
    data = flaskhelper.getargs("data")
    import json

    data = json.loads(data)
    for d in data:
        d=Row(d)

        entity=invite_list
        _columns_ = entity.__dict__['_columns_']
        _pk_columns_=entity.__dict__['_pk_columns_']
        print(type(_pk_columns_))
        if d._state=='modified' :
            for pk in _pk_columns_:
                if pk in d:
                    break
            for c in _columns_:
                if c in d:
                    print('{0}={1}'.format(c,d[c]))

            print('xiugai')
        elif d._state == 'added' :
            
            print(d.invite_code)
            print('add')
        elif d._state=='removed':
            print('delete')

    return "ok"
