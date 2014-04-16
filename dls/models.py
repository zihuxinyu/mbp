# -*- coding: utf8 -*-
import time

from dls import db
from sqlalchemy import Integer
from sqlalchemy.orm.interfaces import MapperExtension
import datetime
from flask import  g

class Snlist(db.Model):
    __tablename__ = 'DLS_SNLIST'
    #SELECT `user_id`, `serial_number`, `develop_depart_id`, `open_date`, `user_state_codeset`, `state_name` FROM
    # `DLS_SNLIST` WHERE 1
    user_id = db.Column('user_id', unique=True, primary_key=True)
    serial_number = db.Column('serial_number')
    develop_depart_id = db.Column('develop_depart_id')
    open_date = db.Column('open_date')
    user_state_codeset = db.Column('user_state_codeset')
    state_name = db.Column('state_name')





class Staff(db.Model):
    __tablename__ = 'dls_staff_chnl'
    staff_id = db.Column('staff_id')
    chnl_id = db.Column('chnl_id')
    chnl_name = db.Column('chnl_name')
    linkman_phone = db.Column('linkman_phone')
    msg = db.Column('msg')
    msgexpdate = db.Column('msgexpdate')

    def __int__(self, staff_id=None, chnl_id=None, chnl_name=None, linkman_phone=None, msg=None, msgexpdate=None):
        self.staff_id = staff_id
        self.chnl_id = chnl_id
        self.chnl_name = chnl_name
        self.linkman_phone = linkman_phone
        self.msg = msg
        self.msgexpdate = msgexpdate


    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.staff_id)

    def __init__(self, staff_id, chnl_id, chnl_name):
        self.staff_id = staff_id
        self.chnl_id = chnl_id
        self.chnl_name = chnl_name
        #self.password= hashlib.md5(password)  #呵呵，这样在插入数据自动给密码哈希了！

    def __repr__(self):
        return "<Staff '{:s}'>".format(self.staff_id)


class WechatUser(db.Model):
    #SELECT  `source`, `usercode`, `username`, `code` FROM `wechat_user` WHERE 1
    __tablename__ = "wechat_user"
    source = db.Column('source', primary_key=True, unique=True)
    usercode = db.Column('usercode')
    username = db.Column('username')
    code = db.Column('code')
    checked = db.Column('checked')

    def __init__(self, source=None, usercode=None, username=None, code=None, checked=0):
        self.source = source
        self.usercode = usercode
        self.username = username
        self.code = code
        self.checked = checked



class WechatReceive(db.Model):
    # SELECT
    # `guid`, `id`, `target`, `source`, `time`, `raw`, `type`, `content`, `img`, `title`, `description`, `url`,
    # `location`, `scale`, `label`, `ckey`, `Latitude`, `Longitude`, `LPrecision`, `media_id`, `format`, `recognition`
    #
    # FROM
    # `wechat_receive`
    # WHERE
    # 1
    __tablename__ = 'wechat_receive'
    guid = db.Column(Integer, unique=True, primary_key=True, autoincrement=True)
    id = db.Column('id')
    target = db.Column('target')
    source = db.Column('source')
    time = db.Column('time')
    raw = db.Column('raw')
    type = db.Column('type')
    content = db.Column('content')
    img = db.Column('img')
    title = db.Column('title')
    description = db.Column('description')
    url = db.Column('url')
    location = db.Column('location')
    scale = db.Column('scale')
    label = db.Column('label')
    ckey = db.Column('ckey')
    Latitude = db.Column('Latitude')
    Longitude = db.Column('Longitude')
    LPrecision = db.Column('LPrecision')
    media_id = db.Column('media_id')
    format = db.Column('format')
    recognition = db.Column('recognition')

    def __init__(self, id=None, target=None, source=None, time=None, raw=None, type=None, content=None,
                 img=None, title=None, description=None, url=None, location=None, scale=None, label=None, ckey=None,
                 latitude=None, longitude=None, lprecision=None, media_id=None, format=None, recognition=None):
        self.id = id
        self.target = target
        self.source = source
        self.time = time
        self.raw = raw
        self.type = type
        self.content = content
        self.img = img
        self.title = title
        self.description = description
        self.url = url
        self.location = location
        self.scale = scale
        self.label = label
        self.ckey = ckey
        self.latitude = latitude
        self.longitude = longitude
        self.lprecision = lprecision
        self.media_id = media_id
        self.format = format
        self.recognition = recognition















