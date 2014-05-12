# -*- coding: utf-8 -*-

from autodb.models import portal_user
from Library.mailhelper import sendMail, sendMail_Nosync
from flask import  flash
import  requests
def sendsmscode(user_code=None, code=None):
    """
    给user_code的手机号发送验证码code
    :param user_code:
    :param code:
    """
    xx = portal_user.query.filter(portal_user.user_code == user_code).first()
    if xx:
        flash('接收短信手机尾号'+xx.user_mobile[5:])
        data={'smscode':code,'phone':'15605468613'}
        #data={'smscode':code,'phone': xx.linkman_phone}
        requests.post('http://127.0.0.1:6999',data=data)