# coding: utf-8
'''
定时接收附件,有附件就执行
接收规则
{host}#{db}#{table}
134.44.36.190#DLS#portal_user
'''
import os
from Library.mailhelper import  getAttach
from Library.ziphelper import extractfile

path = 'tmp/'
cmd= 'mysql -u root -p9Loveme? DLS < ./{0}'


# 读取邮件
getAttach(prefx='134.44.36.190#DLS#',path=path)


for filename in os.listdir(path):
    if filename.endswith('.zip'):
        #解压并删除
        extractfile(filepath=path, zipname=filename)
for filename in os.listdir(path):
    if filename.endswith('.sql'):
        #执行sql语句
        os.system(cmd.format(path+filename))


