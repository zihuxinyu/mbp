# -*- coding: utf-8 -*-

from dls.models import Staff
from Library.mailhelper import sendMail, sendMail_Nosync
from flask import  flash

def sendsmscode(user_code=None, code=None):
    """
    给user_code的手机号发送验证码code
    :param user_code:
    :param code:
    """
    xx = Staff.query.filter(Staff.staff_id == user_code).first()
    if xx:
        flash('接收短信手机尾号'+xx.linkman_phone[5:])
        #sendstr = 'MSG#{0}#{1}'.format(xx.linkman_phone, code)
        sendstr = 'MSG#{0}#{1}'.format('15605468613', code)
        sendMail_Nosync(sendstr,sendstr)
