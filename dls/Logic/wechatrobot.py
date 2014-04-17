# coding: utf-8
import requests
from dls import db, robot
from dls.Logic.WechatLogic import SendGuid, SaveMessage,CheckUser,SendBDPage,SendSnList
from dls.models import WechatUser, WechatReceive


@robot.handler
def echo(message):

    return '您发送了此{0}'.format(message.type)





@robot.text
def echo(message, session):
    SaveMessage(message)

    w = CheckUser(message.source)
    if not w:
        return SendBDPage(message)

    return  process(message)



def process(message):
    if message.content == '查询':
       return SendSnList(message)
    else:
        return SendGuid(message)





@robot.click
def echo(message, session):

    wechat = WechatReceive(id=message.id, target=message.target,
                           source=message.source, time=message.time,
                           raw=message.raw, type=message.type,
                           latitude=message.Latitude, ckey=message.key,
                           longitude=message.Longitude, lprecision=message.Precision
    )
    db.session.add(wechat)
    db.session.commit()
    return str(wechat.guid) + message.key





@robot.subscribe
def echo(message):
    return "welcome"


@robot.unsubscribe
def echo(message):
    return "Bye"