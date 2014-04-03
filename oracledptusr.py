# coding: utf-8

import  tornoracle3


def db():
    return tornoracle3.Connection(host='134.44.36.51',
                                 port='1521',
                                 database='dydb',
                                 user='weibh',
                                 password='1234')

if __name__ == "__main__":


    xx=db().get("select * from oraclerun")
    print(xx.CN)

    man_file = open('man_data.txt', 'w',encoding='utf-8')
    lines=" ({0}, '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', NULL, NULL), \r\n"
    man_file.writelines("TRUNCATE portal_user; INSERT INTO `portal_user` (`guid`, `user_code`, `user_name`, `user_mobile`, `dpt_name`, "
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



