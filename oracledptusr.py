# coding: utf-8
'''
文件作用:定时将oracle dydb的组织架构跑成sql文件,包括删除原数据,插入新数据
'''

import zipfile

from Library.DB import tornoracle3

import os


def db():
    return tornoracle3.Connection(host='134.44.36.51',
                                 port='1521',
                                 database='dydb',
                                 user='weibh',
                                 password='1234')

if __name__ == "__main__":


    man_file = open('tmp/man_data.txt', 'w',encoding='utf-8')
    lines=" ({0}, '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', NULL, NULL), \r\n"
    man_file.writelines("TRUNCATE portal_user;\r\n  INSERT INTO `portal_user` (`guid`, `user_code`, `user_name`, `user_mobile`, `dpt_name`, "
                        "`topdpt`, `manager`, `msg`, `msgexpdate`) VALUES")
    list = db().query("select * from EXT_DPT_USR t")
    i=1
    for x in list:
        #去除最后的逗号
        l=len(list)
        lines=lines.rstrip(', \r\n') if (i==l) else lines

        man_file.writelines(lines.format(i,x.user_code,x.user_name,x.user_mobile,x.dpt_name,x.topdpt,x.manager))
        i=i+1

    man_file.close()

    #压缩文件打包
    zipFile = zipfile.ZipFile(r'tmp/test.zip', 'w')
    zipFile.write(r'tmp/man_data.txt', 'sql.sql', zipfile.ZIP_DEFLATED)
    zipFile.close()
    #删除文件
    os.remove('tmp/man_data.txt')


