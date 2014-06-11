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





def log(fun):
    @functools.wraps(fun)
    def wrapped(*args, **kws):
        print 'before.' + str(args)

        pname = "{0}.{1}".format(fun.__module__, fun.__name__).replace("autodb.views.", "")
        # print(pname)
        # print(getRouters()[pname])
        print(g.user.user_code,g.user.get_groupdid())
        print(pname,checkRights(pname, 2))
        if checkRights(pname, 1):
            retVal = fun(*args, **kws)
            print 'after. ' + str(args)
            return retVal
        else:
            return "No permission"

    return wrapped

@cache.memoize()
@db_session
def checkRights(modulename, groupid):
    """
    检查用户角色是否有模块访问权限
    :param module:
    :param usergroupid
    """

    moduleid = getModuleidByname(modulename)
    if moduleid:
        #存在此模块权限定义
        data = gm.get(moduleid=moduleid, groupid=groupid)
        if data:
            #存在此模块与角色对应赋权
            return True
        else:
            return False
    else:
        #不存在此模块权限定义
        return False


@db_session
@cache.memoize()
def getModuleidByname(modulename):
    """
    通过模块名称获取模块ID
    :param modulename:
    """

    data= modulelist.get(module=modulename)
    if data:
        return data.guid
    else:
        return False



@cache.memoize(10)
def getRouters():
    """
    获取当前app注册的所有route信息，得到具体的route对应module关系

    :return:
    """
    list = [x.split('->') for x in str(app.__dict__['url_map'])
        .replace('Map([', '').replace('])', '')
        .replace('<Rule', '')
        .replace(',', '').replace("'", '').replace("  ", "")
        .replace("HEAD", "").replace("POST", "").replace("OPTIONS", "").replace("GET", "")
        .replace(',', '').replace("'", '').replace("  ", "")
        .replace("()", "")
        .replace("( )", "")
        .strip(' ')
        .split('\n')]

    routers = {x[1].rstrip('>').strip(' '): x[0].strip(' ') for x in list}
    return routers
