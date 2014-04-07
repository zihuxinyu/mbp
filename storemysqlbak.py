# coding: utf-8
'''
定时接收附件,有附件就保存,并发送到ftp
接收规则
BACKUP#{host}#DB
BACKUP#134.44.36.190#DB
此文件接收所有的备份信息
'''


def main():
    import os
    from Library.mailhelper import getAttach
    from Library.ftphelper import ftp_up

    path = os.path.abspath(os.path.dirname(__file__)) + '/bak/'


    #AUTOINIP='119.187.191.82'
    #只接收本机的数据内容
    prefx = 'BACKUP#'
    print(prefx)

    # 读取邮件
    getAttach(prefx=prefx, path=path,saveasdate=True)

    for filename in os.listdir(path):
        if  filename.endswith('.zip') and '.all.sql' in filename:
            filecwd='/weibaohui/{0}'.format(filename.split('.all.sql')[0])
            #解压并删除
            #print(filename)
            ftp_up(path+filename,ftpcwd=filecwd)
            os.remove(path + filename)
            pass


if __name__ == '__main__':
    while True:
        import time
        #间隔23分
        main()
        time.sleep(60*23)

        print('DB store over')



