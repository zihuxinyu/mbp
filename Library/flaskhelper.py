# coding: utf-8
'''
description:扩展flask常用功能
Created by weibaohui on 14-5-14.

'''

import json

def getargs2json(data):
    '''
    转换args为json
    '''
    return json.loads(getargs(data))


def getargs(args,default=None,method=None):

    """
    获取request传输的数据
    :param request:request
    :param args:参数
    :param default:默认值
    :param method:request 发送方式
    :return:
    """
    from flask import request
    method=method if method else 'POST'
    if request.method==method:
        return request.form.get(args) if request.form.get(args) else default
    else:
        return request.args.get(args) if request.args.get(args) else default

