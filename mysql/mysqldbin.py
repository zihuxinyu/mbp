# coding: utf-8
'''
定时接收附件,有附件就执行
接收规则
{host}#{db}#{table}
134.44.36.190#DLS#portal_user
'''
def main():
    import os
    from Library.mailhelper import  getAttach
    from Library.ziphelper import extractfile
    from Library.config import DB_USER,DB_PSW,DB_DATEBASE,AUTOINIP


    path =os.path.abspath(os.path.dirname(__file__))+'/tmp/'

    cmd= 'cd {4} && mysql -u {1} -p{2} {3} < ./{0}'

    #AUTOINIP='119.187.191.82'
    #只接收本机的数据内容
    prefx='{0}#{1}'.format(AUTOINIP,DB_DATEBASE)
    print(prefx)

    # 读取邮件
    getAttach(prefx=prefx,path=path)


    for filename in os.listdir(path):
        if filename.endswith('.zip'):
            #解压并删除
            extractfile(filepath=path, zipname=filename)
    for filename in os.listdir(path):
        if filename.endswith('.sql'):
            #执行sql语句
            print(cmd.format(filename, DB_USER, DB_PSW, DB_DATEBASE, path))
            os.system(cmd.format(filename,DB_USER,DB_PSW,DB_DATEBASE,path))
            os.remove(path+filename)

if __name__=='__main__':
    while True:
        import time
        #间隔10分
        main()
        time.sleep(600)

        print('DB sync over')



