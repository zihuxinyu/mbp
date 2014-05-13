# coding: utf-8
from pony.orm import *
import cx_Oracle
from Library.config import O_host,O_port,O_database,O_user,O_password
from datetime import  datetime
import uuid

dsn = cx_Oracle.makedsn(O_host, O_port, O_database)

db = Database('oracle', O_user, O_password, dsn)
# db = Database('oracle', user=O_user, password=O_password, dsn=dsn)

class EXT_SMSLOG(db.Entity):
    guid=PrimaryKey(unicode)
    content=Required(unicode)
    creatorid=Required(unicode)
    createdate = Optional(datetime)

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
    and p.content=='ssss' and p.createdate is not None
    ).order_by(desc(EXT_SMSLOG.createdate))[:20].show()
    # select((p.creatorid,count(p)) for p in EXT_SMSLOG).order_by(2).show()
    # x= "count(p.user_code) for p in EXT_DPT_USR"
    # d=select(x).first()
    # print(type(d))



@db_session
def EXT_SMSLOGManager():

    db.insert("EXT_SMSLOG",GUID=str(uuid.uuid4()), CONTENT='22', CREATORID='weibh', CREATEDATE=datetime.now())
    db.commit()


EXT_SMSLOGManager();
print('dddddddddddd')
with db_session:
    ##新增了
    ss=EXT_SMSLOG(content="ssss",guid=str(uuid.uuid4()), creatorid="weibh")
    print(ss)