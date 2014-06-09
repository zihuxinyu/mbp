# coding: utf-8
from datetime import  datetime
from uuid import UUID,uuid4
import cx_Oracle

from pony.orm import *
from Library.config import O_host,O_port,O_database,O_user,O_password


dsn = cx_Oracle.makedsn(O_host, O_port, O_database)

db = Database('oracle', O_user, O_password, dsn)

class EXT_SMSLOG(db.Entity):
    guid = PrimaryKey(unicode, default=str(uuid4()))
    content=Required(unicode)
    creatorid=Optional(unicode)
    createdate = Optional(datetime,default=datetime.now())

class EXT_DPT_USR(db.Entity):
    user_code=PrimaryKey(unicode)
    user_name=Required(unicode)

sql_debug(True)
db.generate_mapping()
show(EXT_SMSLOG)
def userids():
    return ['weibh']
with db_session:
    dpts = select( p.user_code for p in EXT_DPT_USR if p.user_code == 'weibh')[:20]
    data= select(p for p in EXT_SMSLOG if p.creatorid is not None
    and  p.creatorid in userids()
    and p.content=='ssssss'
    ).order_by(desc(EXT_SMSLOG.createdate))[:20].show()
    # select((p.creatorid,count(p)) for p in EXT_SMSLOG).order_by(2).show()
    # x= "count(p.user_code) for p in EXT_DPT_USR"
    # d=select(x).first()
    # print(type(d))



@db_session
def EXT_SMSLOGManager():
    ##新增
    ss = EXT_SMSLOG(content="ssssss",  creatorid="weibh")
    ##TODO:自动进行绑定,自动对某些值进行赋值
    ##print(ss)


#EXT_SMSLOGManager();


