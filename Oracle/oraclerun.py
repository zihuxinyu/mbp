# coding: utf-8
import os
from Library.DB import torndb
from Library.config import DB_HOST, DB_DATEBASE, DB_USER, DB_PSW
from Library.threadinghelper import asyncfun
import cx_Oracle
from Library.config import O_database, O_host, O_password, O_port, O_user
from Library.DB import tornoracle
from Library.datehelper import getOffsetDate, converDateTimeToStr, getLastMonth,now

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'




def dbmysql():
    return torndb.Connection(DB_HOST, DB_DATEBASE, DB_USER, DB_PSW)




def get():

    sql = "select * from sqllist where state=0 and nextexec>='{0}' and nextexec<='{1}'"
    sql = sql.format(now(minutes=-1),now())
    print(sql)
    all = dbmysql().query(sql)
    for x in all:

        #计算下次执行时间,更新状态为0:执行完成
        #更新执行时间,更新状态为1:正在执行
        thdate= now()

        nextdate = nextexec(x.frequency, thdate)
        sqlupdate = "update sqllist set  nextexec='{1}',state=1,lastexec='{2}' where guid={0}"
        dbmysql().execute(sqlupdate.format(x.guid, nextdate,thdate))
        print(x.guid, x.sqlContent)
        #执行sql内容
        execsql(guid=x.guid, sqlContent=x.sqlContent, paras=x.paras)

        sqlupdate = "update sqllist set state=0 where guid={0}"
        dbmysql().execute(sqlupdate.format(x.guid, nextdate, thdate))



@asyncfun
def execsql(guid=None, sqlContent=None, paras=None):
    #执行语句,记录错误
    errorMsglist = OracleExec(sqlContent=sqlContent,paras=paras)
    xx = [(guid, x.sql, x.success, x.message) for x in errorMsglist]
    sqlresult = "insert into `sqlresult` (`sguid`,`sqlContent`,`success`,`message`) values (%s,%s,%s,%s)"
    x = dbmysql().executemany_rowcount(sqlresult, xx)
    #print(xx)




#########################################


def nextexec(frequency=None, lastexec=None):
    frequency = str(frequency)
    lastexec = lastexec if lastexec else now()

    if frequency.startswith('min:'):
        return getnextdate(lastdate=lastexec, minutes=int(frequency.split(':')[1]) * 1)
    else:
        return getnextdate(lastdate=lastexec, minutes=int(frequency.split(':')[1]) * 60)


def getnextdate(lastdate=None, minutes=0):
    from datetime import datetime
    from datetime import timedelta

    lastdate = lastdate if lastdate else  datetime.now()
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
    #    print(subsql)
    return sqlist


def db():
    """
    oracle 带连接池的

    :return:
    """
    return tornoracle.Connection(host=O_host,
                                 port=O_port,
                                 database=O_database,
                                 user=O_user,
                                 password=O_password)


def OracleExec(sqlContent=None, paras=None):
    """
    执行SQL语句,并将结果返回
    :param sqlContent:
    :return:
    """

    import time

    errorMsglist = []
    sqllist = getFormatedSqllist(sqlcontent=sqlContent, paras=paras)
    print(sqllist)

    for i, sql in enumerate(sqllist):
        if sql.strip():
            print(sql)
            time.sleep(1)
            try:
                db().execute(sql)
                errorMsg = ErrorMsg(sql=sql, success=True)
                errorMsglist.append(errorMsg)
            except cx_Oracle.DatabaseError as e:
                errorMsg = ErrorMsg(sql=sql, success=False, message=e.message)
                errorMsglist.append(errorMsg)
                pass

    return errorMsglist


class ErrorMsg:
    '''
    定义执行错误的类
    '''

    sql = ''
    message = None
    success = True

    def __init__(self, sql=None, message=None, success=True):
        self.sql = sql
        self.message = message
        self.success = success


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
    sql = sql.replace('$yyMM-1$', getLastMonth()[2:6])
    print(sql)
    return sql
#########################################

if __name__ == "__main__":
    while True:
        import time

        time.sleep(1)
        get();


