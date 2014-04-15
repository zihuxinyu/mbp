# coding: utf-8
'''
文件作用:定时将oracle dydb的组织架构跑成sql文件,包括删除原数据,插入新数据
另给各其他数据库分发同步文件
'''

from Library.ziphelper import getzipfile

from Library.DB import tornoracle3
from Library.config import O_database, O_host, O_password, O_port, O_user,pythonpath
from Library.mailhelper import sendMail

import os
import time

path = pythonpath + '/bak/'



def db():
    return tornoracle3.Connection(host=O_host,
                                  port=O_port,
                                  database=O_database,
                                  user=O_user,
                                  password=O_password)


def sendportal():
    """
    为各数据库提供组织架构的同步

    """
    #目的mysql表名
    tablename = "portal_user"
    #从源数据库获取语句
    selectsql = 'select rownum as guid, user_code, user_name, user_mobile, dpt_name, topdpt, manager, NULL as msg, ' \
                'opdate as msgexpdate  from Ext_dpt_usr'
    #发送出去
    host_database={'autodb':'134.44.36.190','zcgl':'119.187.191.82'}
    senddbzip(tablename=tablename,selectsql=selectsql, host_database=host_database)


def sendDLS():

    #从源数据库获取语句
    selectsql = 'select * from DLS_SNLIST'

    #目的mysql表名
    tablename = "dls_snlist"

    #发送出去
    host_database = {'dls': '119.187.191.82', 'dls': '134.44.36.190'}
    senddbzip(tablename=tablename, selectsql=selectsql, host_database=host_database)



def senddbzip(tablename, selectsql, host_database={}):
    """
    将同步文件发送出去
    :param tablename:同步数据库表的名称
    :param selectsql:数据来源,注意select 中字段要和tablename中一致
    :param host_database:字典,格式为 数据库名:服务器IP
    host_database = {'autodb': '134.44.36.190', 'zcgl': '119.187.191.82'}

    """

    #sql文件路径
    _tmpsqlpath = path + '{0}.sql'.format(tablename)


    #定义sql文件模板
    _head = "SET NAMES utf8;TRUNCATE {0};\r\nINSERT INTO `{0}` ({1}) VALUES "
    _lines = "({0}), \r\n"

    #取得所有列
    columns = db().getcolumn_names(selectsql)
    _columns = ','.join(['`{0}`'.format(c.lower()) for c in columns])
    head = _head.format(tablename, _columns)

    man_file = open(_tmpsqlpath, 'w', encoding='utf-8')
    man_file.writelines(head)

    list = db().query(selectsql)
    i = 1
    for x in list:
        #去除最后的逗号
        #print(','.join([('\'{0}\'').format(str(x[c])) for c in columns]))
        l = len(list)
        _lines = _lines.rstrip(', \r\n') if (i == l) else _lines
        man_file.writelines(_lines.format(','.join([('\'{0}\'').format(str(x[c])) for c in columns])))
        i += 1

    man_file.close()




    #每个数据库一个sql文件,最后分别压缩后发送
    #格式要求table.db.sql,导入是判断以db.sql结尾来确认
    _realsqlpath = path + '{0}.{1}.sql'

    #压缩包地址
    tmpzippath = path + '{0}.zip'.format(tablename)



    for d in host_database:
        print(d,host_database[d])
        realsqlpath = _realsqlpath.format(tablename, d)
        print(realsqlpath)
        open(realsqlpath, "wb").write(open(_tmpsqlpath, "rb").read())
        #压缩文件打包
        getzipfile(filepath=realsqlpath, zipname=tmpzippath)
        #删除文件
        os.remove(realsqlpath)
        subject = '{host}#{db}#{table}'.format(host=host_database[d], db=d, table=tablename)
        sendMail(subject, tablename, tmpzippath)
        #os.remove(tmpzippath)#多线程的删除可能会有问题

if __name__ == "__main__":

    while True:
        #1小时执行一次

        sendportal()
        sendDLS()
        time.sleep(60 * 60 * 1)
        print('send sync db over')
        #time.sleep(120)
        pass