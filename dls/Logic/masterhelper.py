# coding: utf-8
from  flask import  g
from mbp.models import usergroup
def islogin():
    """
    检查是否登陆

    :return: 用户或者None
    """
    return g.user.get_id()
def chkright():
    pass