# -*- coding: utf-8 -*-

from flask_mail import Message
from mbp import mail, app
from decos import asyncfun
from mbp.models import portal_user


@asyncfun
def send_async_email(msg):
    """

    :type msg: object
    """
    mail.send(msg)


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

    """
    给user_code的手机号发送验证码code
    :param user_code:
    :param code:
    """
    xx = portal_user.query.filter(portal_user.user_code == user_code).first()
    if xx:
        sendstr = 'MSG#{0}#{1}'.format(xx.user_mobile, code)
        send_email(sendstr, 'sd-lcgly@chinaunicom.cn',
                   ['sd-lcgly@chinaunicom.cn'], sendstr,
                   sendstr)
