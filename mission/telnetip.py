# -*- coding: utf-8 -*- 

import telnetlib
import time

'''Telnet远程登录：Windows客户端连接Linux服务器'''

# 配置选项

def noarp(Host,ips):
    username = 'weibaohui'  # 登录用户名
    password = 'baohui'  # 登录密码

    # 连接Telnet服务器
    tn = telnetlib.Telnet(Host)
    #tn.set_debuglevel(2)
    # 输入登录用户名
    tn.read_until('Username: ')
    tn.write(username + '\n')

    # 输入登录密码
    tn.read_until('Password: ')
    tn.write(password + '\n')
    tn.write( 'en\n')
    tn.read_until('Password: ')
    tn.write(password + '\n')
    tn.write('config t \n')

    for ip in ips:
        tn.write('no arp  {0} \n'.format(ip))
    tn.write('end\n')
    tn.write('copy run start\n')
    tn.write('\n')
    tn.write('quit\n')

    tn.close()


if __name__ == "__main__":

    iplist={"134.44.208.254":['134.44.208.250','134.44.208.180']    }
    while True:

        for li in iplist:
            noarp(li,iplist[li])
        time.sleep(60*60)