# coding: utf-8
'''
网络操作类程序
'''
import socket

def getlocalip():
    """
    获取本机IP地址

    :return:
    """
    localIP = socket.gethostbyname(socket.gethostname())  #得到本地ip
    return localIP