# coding: utf-8

import  tornoracle


def db():
    return tornoracle.Connection(host='134.44.36.51',
                                 port='1521',
                                 database='dydb',
                                 user='weibh',
                                 password='1234')







if __name__ == "__main__":
    list= db().query("select * from EXT_LOGINLOG t")
    for x in list:
        print(unicode(x.user_name,"utf-8").encode('utf-8'), str(x.createdate))
        pass
    xx=db().get("select * from oraclerun")
    print(xx.opdate)



