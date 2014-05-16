# coding: utf-8

import  random
import string

def generate_code(length=4):
    """
    产生随机字数字字符

    :return:
    """
    passwd = []
    while (len(passwd) < length):
        passwd.append(random.choice(string.digits))
    return ''.join(passwd)





def PadLeft(str, num, padstr):
    '''
    扩展为C#中的String.PadLeft
    '''
    stringlength = len(str)
    n = num - stringlength
    if n >= 0:
        str = padstr * n + str
    return str