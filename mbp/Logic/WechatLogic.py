# -*- coding: utf8 -*-
import random
import string
from mbp import db
from sqlalchemy import and_
from mbp.models import WechatUser, WechatReceive


def SaveMessage(message,imgcontent=None):
    if message.type=="text":
        #收到文本
        wechat = WechatReceive(id=message.id, target=message.target,
                               source=message.source, time=message.time,
                               raw=message.raw, type=message.type,
                               content=message.content
        )
    elif message.type=="image":
        #图像
        wechat = WechatReceive(id=message.id, target=message.target,
                               source=message.source, time=message.time,
                               raw=message.raw, type=message.type,
                               content=imgcontent, img=message.img
        )
    elif message.type=="location":
        #地图位置
        wechat = WechatReceive(id=message.id, target=message.target,
                               source=message.source, time=message.time,
                               raw=message.raw, type=message.type,
                               label=message.label
        )

    elif message.type == "link":
        #链接
        wechat = WechatReceive(id=message.id, target=message.target,
                               source=message.source, time=message.time,
                               raw=message.raw, type=message.type,
                               title=message.title, description=message.description,
                               url=message.url
        )
    elif message.type == "voice":
        #声音
        wechat = WechatReceive(id=message.id, target=message.target,
                               source=message.source, time=message.time,
                               raw=message.raw, type=message.type,
                               media_id=message.media_id, format=message.format,
                               recognition=message.recognition
        )

    db.session.add(wechat)
    db.session.commit()
    return wechat.guid


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