# coding: utf-8
'''
description:
Created by weibaohui on 14-6-8.

'''
import functools
from autodb import app


def Loglevel(level):
    print(level)
    def log(fun):
        print 'log: ' + fun.__name__

        def wrapped(*args, **kws):
            print 'before.' + str(args)

            retVal = fun(*args, **kws)
            print 'after. ' + str(args)
            return retVal

        return wrapped
    return log


def log(fun):

    @functools.wraps(fun)
    def wrapped(*args, **kws):
        print 'before.' + str(args)
        pname= "{0}.{1}".format(fun.__module__, fun.__name__).replace("autodb.views.", "")
        print(pname)
        print(getRouters()[pname])
        #for x in dir(fun):
        #    print(x,getattr(fun,x))
        if  len(pname)<3:
            retVal = fun(*args, **kws)
            print 'after. ' + str(args)
            return retVal
        else:
            return "No permission"
    return wrapped


def getRouters():
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
