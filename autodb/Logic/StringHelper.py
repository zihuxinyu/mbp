# -*- coding: utf8 -*-
'''
扩展为C#中的String.PadLeft
'''


def PadLeft(str, num, padstr):
    stringlength = len(str)
    n = num - stringlength
    if n >= 0:
        str = padstr * n + str
    return str