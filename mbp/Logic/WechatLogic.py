# -*- coding: utf8 -*-
import random
import string
from sqlalchemy import and_
from mbp.models import WechatUser

def generate_code():
    """
    产生随机字符

    :return:
    """
    passwd = []
    while (len(passwd) < 4):
        passwd.append(random.choice(string.digits))
    return ''.join(passwd)


def CheckUser(source):
    """
    检查用户是否绑定了门户账户
    :rtype : Boolean
    :param source:
    """


    w = WechatUser.query.filter(and_(WechatUser.source == source,
                                     WechatUser.checked == 1)).first()
    if w:
        return True
    else:
        return False

def SendBDPage(message):
    """
    产生绑定账户的页面
    :param message:
    :return:
    """
    from werobot.reply import ArticlesReply, Article, create_reply

    reply = ArticlesReply(message=message)
    article = Article(
        title="绑定门户账户",
        description="请输入门户账户进行绑定",
        img="https://github.com/apple-touch-icon-144.png",
        url='http://dyit.org/bd/' + message.source
    )
    reply.add_article(article)
    return reply