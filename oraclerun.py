# coding: utf-8
from config import DB_HOST, DB_DATEBASE, DB_USER, DB_PSW
from decos import asyncfun
from mbp.Logic import DateLogic
import torndb
import cx_Oracle
def db():
    return torndb.Connection(DB_HOST, DB_DATEBASE, DB_USER, DB_PSW)

def get():
    from mbp.Logic.SqlListLogic import nextexec
    sql="select * from sqllist"

    all=db().query(sql)
    for x in all:
        #执行sql内容
        execsql(guid=x.guid, sqlContent=x.sqlContent,paras=x.paras)
        #计算下次执行时间
        nextdate = nextexec(x.frequency, x.lastexec)
        sqlupdate = "update sqllist set nextexec='{1}' where guid={0}"
        db().execute(sqlupdate.format(x.guid, nextdate))

@asyncfun
def execsql(guid=None, sqlContent=None,paras=None):
    from mbp.Logic.SqlListLogic import OracleExec


    #更新执行时间
    sqlupdate = "update sqllist set lastexec='{1}' where guid={0}"
    db().execute(sqlupdate.format(guid,DateLogic.now() ))

    #执行语句,记录错误
    errorMsglist=OracleExec(sqlContent,paras)
    xx=[(guid,x.sql,x.success,x.message) for x in errorMsglist]
    sqlresult="insert into `sqlresult` (`sguid`,`sqlContent`,`success`,`message`) values (%s,%s,%s,%s)"
    x=db().executemany_rowcount(sqlresult,xx)
    #print(x)



if __name__=="__main__":
    get();
    eql="{corn},{defx},{abc},{xyz}"
    print(eql.format(corn=33,defx='dfsf',abc='sdsd',xyz=6))
