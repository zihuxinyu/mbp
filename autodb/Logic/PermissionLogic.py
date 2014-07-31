# coding: utf-8
'''
description:
Created by weibaohui on 14-6-8.

'''
import functools
from flask import g
from autodb import app, cache
from pony.orm import *
from autodb.models.portal import group_module as gm
from autodb.models.portal import modulelist
from autodb.models.OracleUser import EXT_USER_GROUP


def power(fun):
    @functools.wraps(fun)
    def wrapped(*args, **kws):
        print 'before.' + str(args)

        pname = "{0}.{1}".format(fun.__module__, fun.__name__).replace("autodb.views.", "")
        #print( fun.__module__+fun.__name__,'modulename')
        if checkRights(pname):
            retVal = fun(*args, **kws)
            print 'after. ' + str(args)
            return retVal
        else:
            return g.user.get_id()+ "没有权限访问此功能"

    return wrapped



def checkRights(modulename):
    """
    检查用户角色是否有模块访问权限
    :param module:
    :param usergroupid
    """

    #得到用户权限
    groupid = getGroupidByUsercode(g.user.get_id())
    #如果是管理员，则取消权限验证
    if '1' in groupid:
        return True

    moduleid = getModuleidByname(modulename)
    if moduleid:
        #存在此模块权限定义

        return getRelation(groupid, modulename)
    else:
        #不存在此模块权限定义，默认不存在的都通过，加入控制的必须要配权限
        return True


@db_session
def getRelation(groupid, modulename):
    """
    通过角色id，模块ID查找对应关系
    有此ID角色可以访问此ID模块，没有说明未授权
    写入modulelist中得都会进行权限认证，没有写进去的不会被控制
    :param groupid:
    :param moduleid:
    :return:
    """
    data = select(p for p in gm if p.modulename == modulename and p.groupid in groupid)
    if data:
        # 存在此模块与角色对应赋权，可以做进一步的功能控制，或者切入按钮级的控制
        return True
    else:
        return False

@db_session
def getGroupidByUsercode(user_code):
    """
    通过User_code获取角色ID
    :param user_code:
    :return:
    """
    data=select(p for p in EXT_USER_GROUP if p.user_code==user_code)


    return  [d.groupid for d in data] if data else False


@db_session
def getModuleidByname(modulename):
    """
    通过模块名称获取模块ID
    :param modulename:
    """

    data= modulelist.get(modulename=modulename)
    if data:
        return data.guid
    else:
        return False


@cache.memoize(10)
def geturlmap():
    '''
    获取路由表
    :return:dict
    '''

    per = {}
    for i in app.url_map._rules:

        if (not i.endpoint.find('static') > -1) and (not i.endpoint.startswith('admin')):
            if per.get(i.endpoint):

                per[i.endpoint]['rule'].append(i.rule)
            else:
                per[i.endpoint] = {}
                per[i.endpoint]['doc'] = app.view_functions[i.endpoint].__doc__
                per[i.endpoint]['rule'] = [i.rule]
    return per

