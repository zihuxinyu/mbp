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

        if checkRights(pname):
            retVal = fun(*args, **kws)
            print 'after. ' + str(args)
            return retVal
        else:
            return "No permission"+g.user.get_id()

    return wrapped



def checkRights(modulename):
    """
    检查用户角色是否有模块访问权限
    :param module:
    :param usergroupid
    """

    moduleid = getModuleidByname(modulename)
    if moduleid:
        #存在此模块权限定义
        groupid=getGroupidByUsercode(g.user.get_id())
        return getRelation(groupid, moduleid)
    else:
        #不存在此模块权限定义，默认不存在的都通过，加入控制的必须要配权限
        return True


@db_session
def getRelation(groupid, moduleid):
    """
    通过角色id，模块ID查找对应关系
    有此ID角色可以访问此ID模块，没有说明未授权
    写入modulelist中得都会进行权限认证，没有写进去的不会被控制
    :param groupid:
    :param moduleid:
    :return:
    """
    data = select(p for p in gm if p.moduleid == moduleid and p.groupid in groupid)
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
