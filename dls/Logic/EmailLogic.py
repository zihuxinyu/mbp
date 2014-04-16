# -*- coding: utf-8 -*-

from flask_mail import Message
from dls import mail, app
from Library.threadinghelper import asyncfun
from dls.models import Staff


'''@asyncfun'''
def send_async_email(msg):
    """

    :type msg: object
    """
    try:
        mail.send(msg)
    except:
        pass

def send_email(subject, sender, recipients, text_body, html_body):
    if not isinstance(subject, unicode):
        subject = unicode(subject)

    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body

    #with app.open_resource("22.jpg") as fp:
    #    msg.attach("image.png", "image/jpg", fp.read())
    send_async_email(msg)
    #thr = threading.Thread(target = send_async_email, args = [msg])
    #thr.start()


def sendsmscode(user_code=None,code=None):
    print(user_code,code)
    #return ""
    """
    给user_code的手机号发送验证码code
    :param user_code:
    :param code:
    """
    xx = Staff.query.filter(Staff.staff_id == user_code).first()
    if xx:
        sendstr = 'MSG#{0}#{1}'.format(xx.linkman_phone, code)
        send_email(sendstr, 'sd-lcgly@chinaunicom.cn',
                   ['sd-lcgly@chinaunicom.cn'], sendstr,
                   sendstr)
