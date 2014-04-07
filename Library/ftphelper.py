#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
import os
from ftplib import FTP
from Library.config import FTP_IP,FTP_PORT,FTP_PSW,FTP_USR

def ftp_up(fullpath="20120904.rar",ftpcwd='Weibaohui/134.44.36.120'):
    """
    上传FTP文件
    :param fullpath:上传文件的完整路径
    :param ftpcwd:ftp切换目录
    """
    ftp = FTP()
    ftp.set_debuglevel(2)  #打开调试级别2，显示详细信息;0为关闭调试信息
    ftp.connect(FTP_IP,int(FTP_PORT))  #连接
    ftp.login(FTP_USR,FTP_PSW)  #登录，如果匿名登录则用空串代替即可

    ftp.cwd(ftpcwd) #选择操作目录
    file_handler = open(fullpath, 'rb')  #以读模式在本地打开文件
    ftp.storbinary('STOR '+fullpath, file_handler)  #上传文件
    ftp.set_debuglevel(0)
    file_handler.close()
    ftp.quit()
    print ("ftp up OK")


def ftp_down(filename="20120904.rar"):
    ftp = FTP()
    ftp.set_debuglevel(2)
    ftp.connect(FTP_IP, FTP_PORT)  #连接
    ftp.login(FTP_USR, FTP_PSW)  #登录，如果匿名登录则用空串代替即可
    #print ftp.getwelcome()#显示ftp服务器欢迎信息 
    #ftp.cwd('xxx/xxx/') #选择操作目录 
    bufsize = 1024
    filename = "20120904.rar"
    file_handler = open(filename, 'wb').write  #以写模式在本地打开文件
    ftp.retrbinary('RETR %s' % os.path.basename(filename), file_handler, bufsize)  #接收服务器上文件并写入本地文件
    ftp.set_debuglevel(0)
    file_handler.close()
    ftp.quit() 