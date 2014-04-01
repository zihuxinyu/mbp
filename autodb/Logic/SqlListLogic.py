# coding: utf-8
import cx_Oracle
from mbp.Logic import DateLogic


def nextexec(frequency=None,lastexec=None):
    frequency=str(frequency)
    lastexec=lastexec if  lastexec else DateLogic.now()

    if frequency.startswith('hour:'):
        return getnextdate(lastdate=lastexec,hours=int(frequency.split(':')[1])*1)
    else:
        return getnextdate(lastdate=lastexec, hours=int(frequency.split(':')[1])*24)

def getnextdate(lastdate=None, hours=0):

    from datetime import datetime
    from datetime import timedelta
    lastdate=lastdate if lastdate else  datetime.now()
    now = datetime.strptime(str(lastdate), '%Y-%m-%d %H:%M:%S')
    aDay = timedelta(minutes=hours*60)
    now = now + aDay
    return now.strftime('%Y-%m-%d %H:%M:%S')


def getFormatedSqllist(sqlcontent):
    '''
    获取格式化后的sql列表，主要去除注释
    '''

    line = sqlcontent
    listx = line.split('\n')
    sql = ''
    for sublist in listx:
        if not sublist.startswith('--'):
            sql += sublist + ' '
            #print(sublist)
    sqlist = sql.split(';')
    #print(sqlist)
    #for subsql in sqlist:
    #    print(subsql)
    return sqlist


def OracleExec(sqlContent=None,paras=None):
    """
    执行SQL语句,并将结果返回
    :param sqlContent:
    :return:
    """

    from mbp.Logic.SqlListLogic import getFormatedSqllist
    from mbp.Logic.SqlListLogic import replacepara

    errorMsglist = []
    sqllist = getFormatedSqllist(sqlContent)

    host = '134.44.36.51'
    port = 1521
    dbase = 'dydb'
    login = 'weibh'
    passwrd = '1234'
    dsn = cx_Oracle.makedsn(host, port, dbase)
    oracledb = cx_Oracle.connect(login, passwrd, dsn, threaded=True)
    oraclecursor = oracledb.cursor()
    for i, sql in enumerate(sqllist):
        if sql.strip():
            import  time
            print('sleep')
            time.sleep(1)
            print('week')
            try:
                sql = replacepara(sql, paras)
                oraclecursor.execute(sql)
                errorMsg = ErrorMsg(sql=sql, success=True)
                errorMsglist.append(errorMsg)
            except cx_Oracle.DatabaseError as e:
                errorMsg = ErrorMsg(sql=sql, success=False,message=e.message)
                errorMsglist.append(errorMsg)
                pass
    oraclecursor.close()
    oracledb.commit()
    oracledb.close()
    return errorMsglist


class ErrorMsg:
    '''
    定义执行错误的类
    '''

    sql=''
    message=None
    success=True
    def __init__(self,sql=None,message=None,success=True):
        self.sql=sql
        self.message=message
        self.success=success


def replacepara(sql=None,paras=None):
    """
    替换格式
    :param sql:
    sql = "$corn$,$defx$,$abc$,$abc$,$abc$,$xyz$"
    paras = "corn=33,defx='sdsdsds'"
    """

    if not paras:
        return sql
    for x in paras.split(','):
        _x = x.split('=')
        old = '$' + _x[0] + '$'
        new = _x[1]
        sql = sql.replace(old, new)
    return sql
