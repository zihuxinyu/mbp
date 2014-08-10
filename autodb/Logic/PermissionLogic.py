# coding: utf-8
'''
description:
Created by weibaohui on 14-6-8.

'''
import functools
import json

from flask import g, abort
from autodb import app, cache
from pony.orm import *
from autodb.models.portal import group_module as gm
from autodb.models.portal import modulelist
from autodb.models.OracleUser import EXT_USER_GROUP, EXT_DPT_USR
from Library.minihelper import getTreeDataInList


def power(fun) :
    @functools.wraps(fun)
    def wrapped(*args, **kws) :
        print 'before.' + str(args)

        pname = "{0}.{1}".format(fun.__module__, fun.__name__).replace("autodb.views.", "")
        # print( fun.__module__+fun.__name__,'modulename')

        # 得到用户权限
        groupid = getGroupidByUsercode(g.user.get_id())
        # 如果是管理员，则取消权限验证
        if '1' in groupid :
            retVal = fun(*args, **kws)
            print '管理员. ' + str(args)
            return retVal

        if checkRights(pname, groupid) :
            retVal = fun(*args, **kws)
            print 'after. ' + str(args)
            return retVal
        else :

            return abort(403)
            return g.user.get_id() + "没有权限访问此功能"

    return wrapped


@cache.memoize(60 * 60)
def checkRights(modulename, groupid) :
    """
    检查用户角色是否有模块访问权限
    :param module:
    :param usergroupid
    """

    moduleid = getModuleidByname(modulename)
    if moduleid :
        # 存在此模块权限定义

        return getRelation(groupid, modulename)
    else :
        # 不存在此模块权限定义，默认不存在的都通过，加入控制的必须要配权限
        return True


@db_session
@cache.memoize()
def getRelation(groupid, modulename) :
    """
    通过角色id，模块ID查找对应关系
    有此ID角色可以访问此ID模块，没有说明未授权
    写入modulelist中得都会进行权限认证，没有写进去的不会被控制
    :param groupid:
    :param moduleid:
    :return:
    """
    data = select(p for p in gm if p.modulename == modulename and p.groupid in groupid)
    if data :
        # 存在此模块与角色对应赋权，可以做进一步的功能控制，或者切入按钮级的控制
        return True
    else :
        return False


@db_session
@cache.memoize(60 * 60 * 24)
def getGroupidByUsercode(user_code) :
    """
    通过User_code获取角色ID
    :param user_code:
    :return:
    """
    data = select(p for p in EXT_USER_GROUP if p.user_code == user_code)

    return [d.groupid for d in data] if data else False


@db_session
@cache.memoize(60 * 60 * 24 * 5)
def getUserInfoByUsercode(user_code) :
    """
    通过User_code获取用户相关信息,包括员工编号、部门、手机号等
    :param user_code:
    :return:
    """
    data = select(p for p in EXT_DPT_USR if p.user_code == user_code)
    for d in data :
        return d if d else False


@db_session
@cache.memoize()
def getModulenameByGroupId(groupid) :
    '''
    通过角色ID获取权限名称
    :param groupid:角色list[]
    :return:list[]
    '''
    from autodb.models.portal import group_module

    data = select(p.modulename for p in group_module if p.groupid in groupid)[:]
    return data


#@cache.memoize()
def getMenusByUser_code(user_code) :
    '''
    通过用户账号获取对应的菜单
    :param user_code:
    :return:
    '''
    groupid = getGroupidByUsercode(user_code)
    modulenames = getModulenameByGroupId(groupid)
    menulist = []
    getMenuList(menulist, filter = modulenames)
    ids,return_menu=[],[]
    for x in menulist:
        if x["id"] not in ids:
            ids.append(x['id'])
            return_menu.append(x)
    return json.dumps(return_menu)


@db_session
# @cache.memoize()
def getMenuList(menulist = [], pid = None, filter = []) :

    '''

    迭代获取菜单关系
    没有注明modulename的菜单认为所有角色都可以使用
    :param menulist:  存放菜单的list
    :param pid: 父菜单ID,默认顶级菜单为0
    :param filter: 过滤
    :return:
    '''
    from autodb.models.portal import menutree
    #
    # data = select(p for p in menutree if p.pid == pid).order_by(menutree.num)
    # datajson = getTreeDataInList(menutree, data)
    # for x in datajson :
    # if x["modulename"] == "" or x["modulename"] in filter :
    #         menulist.append(x)
    #         getMenuList(menulist, x['id'], filter)

    if filter :
        data = select(p for p in menutree if p.modulename in filter).order_by(menutree.num)
    else :
        data = select(p for p in menutree if p.id == pid ).order_by(menutree.num)
    datajson = getTreeDataInList(menutree, data)
    for x in datajson :

        menulist.append(x)
        getMenuList(menulist, pid = x['pid'])


@db_session
@cache.memoize(60 * 60 * 24)
def getModuleidByname(modulename) :
    """
    通过模块名称获取模块ID
    :param modulename:
    """

    data = modulelist.get(modulename = modulename)
    if data :
        return data.guid
    else :
        return False


# @cache.memoize(60 * 60 * 24)
def geturlmap() :
    '''
    获取路由表
    :return:dict
    '''

    per = { }
    for i in app.url_map._rules :
        # 对所有注册的模块进行权限控制
        # print('geturlmap',i.methods,type(i.methods))
        # if 'GET' not in i.methods:
        # #只保留具有get属性的菜单
        #     continue

        if (not i.endpoint.find('static') > -1) and (not i.endpoint.startswith('admin')) :
            if per.get(i.endpoint) :

                per[i.endpoint]['rule'].append(i.rule)
            else :
                per[i.endpoint] = { }
                per[i.endpoint]['doc'] = app.view_functions[i.endpoint].__doc__
                per[i.endpoint]['rule'] = [i.rule]
    return per

