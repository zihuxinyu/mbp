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
    #sql文件路径
    tmpsqlpath =  path+'{0}.sql'.format(tablename)

    realsqlpath = path + '{0}.{1}.sql'
    #压缩包地址
    tmpzippath = path +'{0}.zip'.format(tablename)
    #从源数据库获取语句
    selectsql = 'select * from Ext_dpt_usr'

    head = "SET NAMES utf8;TRUNCATE {0};\r\nINSERT INTO `{0}` (`guid`, `user_code`, `user_name`, `user_mobile`, `dpt_name`, `topdpt`, `manager`, `msg`, `msgexpdate`) VALUES "

    lines = "({0}, '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', NULL, NULL), \r\n"

    man_file = open(tmpsqlpath, 'w', encoding='utf-8')
    man_file.writelines(head.format(tablename))

    list = db().query(selectsql)
    i = 1
    for x in list:
        #去除最后的逗号
        l = len(list)
        lines = lines.rstrip(', \r\n') if (i == l) else lines
        man_file.writelines(lines.format(i, x.user_code, x.user_name, x.user_mobile, x.dpt_name, x.topdpt, x.manager))
        i += 1

    man_file.close()
    #复制到realpath
    to_database = ['autodb','zcgl']
    host_database={'autodb':'134.44.36.190','zcgl':'119.187.191.82'}
    for d in to_database:
        realsqlpath = realsqlpath.format(tablename, d)
        open(realsqlpath, "wb").write(open(tmpsqlpath, "rb").read())
        #压缩文件打包
        getzipfile(filepath=realsqlpath, zipname=tmpzippath)
        #删除文件
        os.remove(realsqlpath)

        subject = '{host}#{db}#{table}'.format(host=host_database[d], db=d, table=tablename)
        #print(subject)
        sendMail(subject, tablename, tmpzippath)

        #os.remove(tmpzippath)#多线程的删除可能会有问题


def sendDLS():


    """
    发送DLS同步数据

    """
    print(path)
    #目的mysql表名
    tablename = "dls_snlist"
    #临时sql文件路径
    tmpsqlpath = path + '{0}.sql'.format(tablename)
    #每个数据库一个sql文件,最后分别压缩后发送
    #格式要求table.db.sql,导入是判断以db.sql结尾来确认

    realsqlpath= path + '{0}.{1}.sql'
    #压缩包地址
    tmpzippath = path + '{0}.zip'.format(tablename)
    #从源数据库获取语句
    selectsql = 'select * from DLS_SNLIST'

    head = "SET NAMES utf8;TRUNCATE {0};\r\nINSERT INTO `{0}` (`user_id`, `serial_number`, `develop_depart_id`, " \
           "`open_date`, `user_state_codeset`, `state_name`,`impdate`) VALUES "

    lines = "('{0}', '{1}', '{2}', '{3}', '{4}', '{5}','{6}'), \r\n"

    man_file = open(tmpsqlpath, 'w', encoding='utf-8')
    man_file.writelines(head.format(tablename))

    list = db().query(selectsql)
    i = 1
    for x in list:
        #去除最后的逗号
        l = len(list)
        lines = lines.rstrip(', \r\n') if (i == l) else lines
        #print(i,x.USER_ID,x.SERIAL_NUMBER,x.DEVELOP_DEPART_ID,x.OPEN_DATE,x.USER_STATE_CODESET,x.STATE_NAME,x.IMPDATE )
        man_file.writelines(lines.format(x.USER_ID, x.SERIAL_NUMBER, x.DEVELOP_DEPART_ID, x.OPEN_DATE,
                                         x.USER_STATE_CODESET, x.STATE_NAME, x.IMPDATE))
        i += 1

    man_file.close()


    #复制到realpath
    to_database=['dls']
    host_database = {'dls': '134.44.36.190'}
    for d in to_database:
        realsqlpath=realsqlpath.format(tablename,d)
        open(realsqlpath, "wb").write(open(tmpsqlpath, "rb").read())
        #压缩文件打包
        getzipfile(filepath=realsqlpath, zipname=tmpzippath)
        #删除文件
        os.remove(realsqlpath)
        subject = '{host}#{db}#{table}'.format(host=host_database[d], db=d, table=tablename)
        sendMail(subject, tablename, tmpzippath)
        #os.remove(tmpzippath)#多线程的删除可能会有问题


if __name__ == "__main__":

    while True:
        #5小时执行一次

        sendportal()
        sendDLS()
        time.sleep(60 * 60 * 1)
        #time.sleep(120)
        pass