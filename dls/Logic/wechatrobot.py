# coding: utf-8
import requests
from mbp import db, robot
from dls.Logic.WechatLogic import SaveMessage,CheckUser,SendBDPage
from dls.models import WechatUser, WechatReceive


@robot.handler
def echo(message):

    return '抱歉,未能成功识别此{0},请重试'.format(message.type)


@robot.image
def echo(message):

    return ""


@robot.text
def echo(message, session):
    SaveMessage(message)
    w = CheckUser(message.source)
    if not w:
        return SendBDPage(message)
    if not can_return(message):
        return "您不在清查人员之内,请联系当地资产管理员"
    #先对输入的文字进行二维码提取.
    bar = GetUnicomBarcode(message.content)
    if bar:
        SaveBarcode(barcodelist=bar, message=message,
                    type='input')
        return ShowBarDetail(barcodelist=bar,
                             message=message)

    return message.content


@robot.link
def echo(message, session):
    if not can_return(message):
        return "您不在清查人员之内,请联系当地资产管理员"
    SaveMessage(message)
    return message.url


@robot.location
def echo(message, session):
    if not can_return(message):
        return "您不在清查人员之内,请联系当地资产管理员"
    SaveMessage(message)
    return message.label


@robot.click
def echo(message, session):
    if not can_return(message):
        return "您不在清查人员之内,请联系当地资产管理员"
    wechat = WechatReceive(id=message.id, target=message.target,
                           source=message.source, time=message.time,
                           raw=message.raw, type=message.type,
                           latitude=message.Latitude, ckey=message.key,
                           longitude=message.Longitude, lprecision=message.Precision
    )
    db.session.add(wechat)
    db.session.commit()
    return str(wechat.guid) + message.key


@robot.voice
def echo(message, session):
    if not can_return(message):
        return "您不在清查人员之内,请联系当地资产管理员"
    SaveMessage(message)
    #return  message.media_id
    return '我听见了.'


@robot.subscribe
def echo(message):
    return "welcome"


@robot.unsubscribe
def echo(message):
    return "Bye"