# -*- coding: utf-8 -*-

from mbp.models import portal_user
from Library.mailhelper import sendMail,sendMail_Nosync





def sendsmscode(user_code=None,code=None):

    """
    给user_code的手机号发送验证码code
    :param user_code:
    :param code:
    """
    xx = portal_user.query.filter(portal_user.user_code == user_code).first()
    if xx:
        sendstr = 'MSG#{0}#{1}'.format(xx.user_mobile, code)
        sendMail_Nosync(sendstr,sendstr)
