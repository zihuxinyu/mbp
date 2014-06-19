# coding: utf-8
import os
import sys


reload(sys)
sys.setdefaultencoding('utf-8')
from Library.DB import torndb
from Library.config import DB_HOST, DB_DATEBASE, DB_USER, DB_PSW
from Library.threadinghelper import asyncfun
import cx_Oracle
from Library.config import O_database, O_host, O_password, O_port, O_user
from Library.datehelper import getOffsetDate, converDateTimeToStr, getLastMonth, now

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
from datetime import datetime
from datetime import timedelta
from pony.orm import *


def dbmysql():
    return torndb.Connection(DB_HOST, DB_DATEBASE, DB_USER, DB_PSW)


def db():
    """
    oracle 带连接池的

    :return:
    """
    dsn = cx_Oracle.makedsn(O_host, O_port, O_database)

    dbs = Database('oracle', O_user, O_password, dsn)

    return dbs

def before_process(x):
    """
    oracle 语句执行前
    :param x:
    :return:
    """
    thdate = now()
    nextdate = nextexec(x.frequency, thdate)
    sqlupdate = "update sqllist set nextexec='{1}',state=1,lastexec='{2}' where guid={0}"
    dbmysql().execute(sqlupdate.format(x.guid, nextdate, thdate))
    return nextdate, thdate


def after_process(nextdate, thdate, x):
    """
    oracle 语句执行后
    :param nextdate:
    :param thdate:
    :param x:
    """
    sqlupdate = "update sqllist set state=0 where guid={0}"
    dbmysql().execute(sqlupdate.format(x.guid, nextdate, thdate))


def commit_result(errorMsglist, guid, x):
    """
    提交sql语句执行结果
    :param errorMsglist:
    :param guid:
    :param x:
    :return:
    """
    xx = [(guid, x.sql, x.success, x.message, x.opdate) for x in errorMsglist]
    sqlresult = "insert into `sqlresult` (`sguid`,`sqlContent`,`success`,`message`,`opdate`) values (%s,%s,%s,%s,%s)"
    x = dbmysql().executemany_rowcount(sqlresult, xx)
    return x




def get():
    sql = "select * from sqllist where state=0 and nextexec>='{0}' and nextexec<='{1}'"
    sql = sql.format(now(minutes=-1), now())
    all = dbmysql().query(sql)
    for x in all:
        OracleExec(x)


def nextexec(frequency=None, lastexec=None):
    frequency = str(frequency)
    lastexec = lastexec if lastexec else now()

    if frequency.startswith('min:'):
        return getnextdate(lastdate=lastexec, minutes=int(frequency.split(':')[1]) * 1)
    else:
        return getnextdate(lastdate=lastexec, minutes=int(frequency.split(':')[1]) * 60)


def getnextdate(lastdate=None, minutes=0):


    lastdate = lastdate if lastdate else datetime.now()
    now = datetime.strptime(str(lastdate), '%Y-%m-%d %H:%M:%S')
    aDay = timedelta(minutes=minutes)
    now = now + aDay
    return now.strftime('%Y-%m-%d %H:%M:%S')


def getFormatedSqllist(sqlcontent, paras=None):
    '''
获取格式化后的sql列表，主要去除注释
'''
    line = sqlcontent
    listx = line.split('\n')
    sql = ''
    for sublist in listx:
        if not sublist.startswith('--'):
            #替换sql语句中得值
            sublist = replacepara(sql=sublist, paras=paras)
            sql += sublist + ' '

    sqlist = sql.split(';')
    #for subsql in sqlist:
    # print(subsql)
    return sqlist








@asyncfun
def OracleExec(x):
    """
执行SQL语句,并将结果返回
:param sqlContent:
:return:
"""

    #更新任务状态
    nextdate, thdate = before_process(x)

    guid=x.guid
    sqlContent=x.sqlContent
    paras=x.paras


    errorMsglist = []
    sqllist = getFormatedSqllist(sqlcontent=sqlContent, paras=paras)
    #print(sqllist)
    for i, sql in enumerate(sqllist):
        if sql.strip():
            print(i, len(sqllist))
            print(sql)

            try:
                with db_session:
                    db().execute(sql)
                    errorMsg = ErrorMsg(sql=sql, success=True,opdate=datetime.now())
                    errorMsglist.append(errorMsg)
            except:
                info = sys.exc_info()
                message="{0}:{1}".format( info[0], info[1])
                print(message)
                errorMsg = ErrorMsg(sql=sql, success=False, message=message,opdate=datetime.now())
                errorMsglist.append(errorMsg)
                pass
            #提交执行结果
            commit_result(errorMsglist, guid, x)
        else:
            print(i, len(sqllist),"无")
    #更新任务状态
    after_process(nextdate, thdate, x)


class ErrorMsg:
    '''
定义执行错误的类
'''

    sql = ''
    message = None
    success = True
    opdate=now()

    def __init__(self, sql=None, message=None, success=True,opdate=None):
        self.sql = sql
        self.message = message
        self.success = success
        self.opdate=opdate

def replacepara(sql=None, paras=None):
    """
替换格式
:param sql:
sql = "$corn$,$defx$,$abc$,$abc$,$abc$,$xyz$"
paras = "corn=33,defx='sdsdsds'"
"""
    #print(sql,paras)
    if not paras:
        return sql
    if not '=' in paras:
        return sql
    for x in paras.split(','):
        _x = x.split('=')
        old = '$' + _x[0] + '$'
        new = _x[1]
        sql = sql.replace(old, new)


    #替换通用的时间


    #sql = '当前日期:$yyMM$,当前账期$yyMM$,上个账期$yyMM-1$'
    sql = sql.replace('$yyMMdd$', converDateTimeToStr(getOffsetDate(), format='%y%m%d'))
    sql = sql.replace('$yyyyMMdd$', converDateTimeToStr(getOffsetDate(), format='%Y%m%d'))
    sql = sql.replace('$yyyy-MM-dd$', converDateTimeToStr(getOffsetDate(), format='%Y-%m-%d'))
    sql = sql.replace('$yyMM$', converDateTimeToStr(getOffsetDate(), format='%y%m'))
    sql = sql.replace('$yyyyMM$', converDateTimeToStr(getOffsetDate(), format='%Y%m'))
    sql = sql.replace('$yyyy-MM$', converDateTimeToStr(getOffsetDate(), format='%Y-%m'))
    sql = sql.replace('$yy-MM$', converDateTimeToStr(getOffsetDate(), format='%y-%m'))
    sql = sql.replace('$yyyy$', converDateTimeToStr(getOffsetDate(), format='%Y'))

    days = int(converDateTimeToStr(getOffsetDate(), format='%d'))

    sql = sql.replace('$yyMM-1$', converDateTimeToStr(getOffsetDate(-days), format='%y%m'))
    sql = sql.replace('$yyyyMM-1$', converDateTimeToStr(getOffsetDate(-days), format='%Y%m'))
    print(sql)
    return sql

#########################################

if __name__ == "__main__":
    while True:
        import time

        time.sleep(1)
        get();