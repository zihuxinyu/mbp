# coding: utf-8
'''
定时将数据库进行备份,发送邮件送走
接收规则

'''
def main():
    import os
    from Library.config import DB_USER,DB_PSW,DB_DATEBASE,AUTOINIP
    from Library.mailhelper import sendMail

    path =os.path.abspath(os.path.dirname(__file__))+'/tmp/'
    zipfile='{0}.all.sql.zip'.format(AUTOINIP)
    backcmd='cd {3} && mysqldump -u {1} -p{2} --all-databases | gzip > {0}.all.sql.zip'

    #执行备份
    print(backcmd.format(AUTOINIP, DB_USER, DB_PSW, path))
    os.system(backcmd.format(AUTOINIP, DB_USER, DB_PSW, path))


    #print(subject)
    print(path + zipfile)

    subject = 'BACKUP#{host}#DB'.format(host=AUTOINIP)
    sendMail(subject, subject, path+ zipfile)
    #os.remove(path + zipfile)

if __name__=='__main__':
    import time
    while True:


        main()
        #间隔5小时
        time.sleep(60*60*5)

        print('backup DB over')



