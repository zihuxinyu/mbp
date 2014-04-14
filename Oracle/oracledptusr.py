# coding: utf-8
'''
文件作用:定时将oracle dydb的组织架构跑成sql文件,包括删除原数据,插入新数据
'''

from Library.ziphelper import getzipfile

from Library.DB import tornoracle3
from Library.config import O_database, O_host, O_password, O_port, O_user
import os


def db():
    return tornoracle3.Connection(host=O_host,
                                  port=O_port,
                                  database=O_database,
                                  user=O_user,
                                  password=O_password)


def sendportal():
    path = os.path.abspath(os.path.dirname(__file__)) + '/bak/'
    #目的mysql表名
    tablename = "portal_user"
    #sql文件路径
    tmpsqlpath =  path+'{0}.sql'.format(tablename)
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

    #压缩文件打包
    getzipfile(filepath=tmpsqlpath, zipname=tmpzippath)
    #删除文件
    os.remove(tmpsqlpath)

    from Library.mailhelper import sendMail

    subject = '{host}#{db}#{table}'.format(host='134.44.36.190', db='DLS', table=tablename)
    #print(subject)
    sendMail(subject, tablename, tmpzippath)

    subject = '{host}#{db}#{table}'.format(host='119.187.191.82', db='DLS', table=tablename)
    #sendMail(subject, tablename, tmpzippath)
    os.remove(tmpzippath)#多线程的删除可能会有问题


if __name__ == "__main__":
    import time
    while True:
        #5小时执行一次
        #time.sleep(60*60*1)
        sendportal()
        #time.sleep(120)