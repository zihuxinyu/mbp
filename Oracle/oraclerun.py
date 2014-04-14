# coding: utf-8
from Library.DB import torndb
from Library.config import DB_HOST, DB_DATEBASE, DB_USER, DB_PSW

from decos import asyncfun
from autodb.Logic import DateLogic
import os

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

def db():
    return torndb.Connection(DB_HOST, DB_DATEBASE, DB_USER, DB_PSW)

def pooldb(sql):
    from DBUtils.PooledDB import PooledDB
    from Library.config import O_database, O_host, O_password, O_port, O_user

    import cx_Oracle
    dsn= cx_Oracle.makedsn(O_host, O_port, O_database)
    pool = PooledDB(cx_Oracle, user=O_user, password=O_password, dsn=dsn, mincached=2,
                    maxcached=2, maxshared=2, maxconnections=2)


    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute(sql)

    conn.close();


def get():
    from autodb.Logic.SqlListLogic import nextexec

    sql = "select * from sqllist where state=0 and nextexec>='{0}' and nextexec<='{1}'"
    sql = sql.format(DateLogic.now(minutes=-1),DateLogic.now())
    print(sql)
    all = db().query(sql)
    for x in all:

        #计算下次执行时间,更新状态为0:执行完成
        #更新执行时间,更新状态为1:正在执行
        thdate= DateLogic.now()

        nextdate = nextexec(x.frequency, thdate)
        sqlupdate = "update sqllist set  nextexec='{1}',state=1,lastexec='{2}' where guid={0}"
        db().execute(sqlupdate.format(x.guid, nextdate,thdate))
        print(x.guid, x.sqlContent)
        #执行sql内容
        execsql(guid=x.guid, sqlContent=x.sqlContent, paras=x.paras)

        sqlupdate = "update sqllist set state=0 where guid={0}"
        db().execute(sqlupdate.format(x.guid, nextdate, thdate))



@asyncfun
def execsql(guid=None, sqlContent=None, paras=None):
    from autodb.Logic.SqlListLogic import OracleExec
    #执行语句,记录错误
    errorMsglist = OracleExec(sqlContent=sqlContent,paras=paras)
    xx = [(guid, x.sql, x.success, x.message) for x in errorMsglist]
    sqlresult = "insert into `sqlresult` (`sguid`,`sqlContent`,`success`,`message`) values (%s,%s,%s,%s)"
    x = db().executemany_rowcount(sqlresult, xx)
    print(xx)


if __name__ == "__main__":
    while True:
        import time

        time.sleep(1)
        get();


