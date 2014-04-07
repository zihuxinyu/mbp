# coding: utf-8
__author__ = 'weibaohui'

import  random
import string

def generate_code():
    """
    产生随机字数字字符

    :return:
    """
    passwd = []
    while (len(passwd) < 4):
        passwd.append(random.choice(string.digits))
    return ''.join(passwd)