# coding: utf-8
from config import DB_HOST, DB_DATEBASE, DB_USER, DB_PSW
from decos import asyncfun
from autodb.Logic import DateLogic
import torndb


def db():
    return torndb.Connection(DB_HOST, DB_DATEBASE, DB_USER, DB_PSW)


def get():
    from autodb.Logic.SqlListLogic import nextexec

    sql = "select * from sqllist where nextexec='{0}'"
    sql = sql.format(DateLogic.now())
    print(sql)
    all = db().query(sql)
    for x in all:

        #计算下次执行时间,更新状态为0:执行完成
        #更新执行时间,更新状态为1:正在执行
        thdate= DateLogic.now()

        nextdate = nextexec(x.frequency, thdate)
        sqlupdate = "update sqllist set  nextexec='{1}',state=0,lastexec='{2}' where guid={0}"
        db().execute(sqlupdate.format(x.guid, nextdate,thdate))

        #执行sql内容
        execsql(guid=x.guid, sqlContent=x.sqlContent, paras=x.paras)




@asyncfun
def execsql(guid=None, sqlContent=None, paras=None):
    from autodb.Logic.SqlListLogic import OracleExec






    #执行语句,记录错误
    errorMsglist = OracleExec(sqlContent)
    xx = [(guid, x.sql, x.success, x.message) for x in errorMsglist]
    sqlresult = "insert into `sqlresult` (`sguid`,`sqlContent`,`success`,`message`) values (%s,%s,%s,%s)"
    x = db().executemany_rowcount(sqlresult, xx)
    #print(x)


if __name__ == "__main__":
    # while True:
    #     import time
    #
    #     time.sleep(1)
    #     get();
    import  datetime,time
    from autodb.Logic.StringHelper import PadLeft
    from autodb.Logic.DateLogic import getOffsetDate,converDateTimeToStr,getLastMonth
    sql='当前日期:$yyMM$,当前账期$yyMM$,上个账期$yyMM-1$'
    sql = sql.replace('$yyMMdd$', converDateTimeToStr(getOffsetDate(), format='%y%m%d'))
    sql = sql.replace('$yyyyMMdd$', converDateTimeToStr(getOffsetDate(), format='%Y%m%d'))
    sql = sql.replace('$yyyy-MM-dd$', converDateTimeToStr(getOffsetDate(), format='%Y-%m-%d'))
    sql = sql.replace('$yyMM$', converDateTimeToStr(getOffsetDate(), format='%y%m'))
    sql = sql.replace('$yyyyMM$', converDateTimeToStr(getOffsetDate(), format='%Y%m'))
    sql = sql.replace('$yyyy-MM$', converDateTimeToStr(getOffsetDate(), format='%Y-%m'))
    sql = sql.replace('$yy-MM$', converDateTimeToStr(getOffsetDate(), format='%y-%m'))
    sql = sql.replace('$yyMM-1$', getLastMonth()[2:6])
    print()
    print(sql)

