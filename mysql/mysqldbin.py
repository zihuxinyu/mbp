# coding: utf-8
'''
定时接收附件,有附件就执行
接收规则
{host}#{db}#{table}
134.44.36.190#DLS#portal_user
'''
import os
from Library.mailhelper import getAttach
from Library.ziphelper import extractfile
from Library.config import DB_USER, DB_PSW, AUTOINIP,AUTODATABASE,pythonpath
import time
def main(DATABASE=None):



    path = pythonpath+'/tmp/'

    cmd= 'cd {4} && mysql -u {1} -p{2} {3} < ./{0}'

    #AUTOINIP='119.187.191.82'
    #只接收本机的数据内容,不限制哪个数据库
    prefx='{0}#{1}'.format(AUTOINIP,DATABASE)
    #prefx='{0}#'.format(AUTOINIP)
    print(prefx)

    # 读取邮件
    getAttach(prefx=prefx,path=path)


    for filename in os.listdir(path):
        if filename.endswith('.zip'):
            #解压并删除
            extractfile(filepath=path, zipname=filename)
    for filename in os.listdir(path):
        if filename.endswith('{0}.sql'.format(DATABASE)):
            #执行sql语句
            print(cmd.format(filename, DB_USER, DB_PSW, DATABASE, path))
            os.system(cmd.format(filename,DB_USER,DB_PSW, DATABASE,path))
            os.remove(path+filename)

if __name__=='__main__':

    while True:
       for db in AUTODATABASE:
            #自动导入每一个db的同步数据
            #间隔10分
            main(DATABASE=db)
            print('{0} sync over'.format(db))
       time.sleep(600)


