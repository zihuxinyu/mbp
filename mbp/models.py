# -*- coding: utf8 -*-

from mbp import db
from sqlalchemy import Integer

ROLE_USER = 0
ROLE_ADMIN = 1


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


class wiz_user(db.Model):
    __tablename__ = 'wiz_user'
    #    SELECT `invite_code`, `proxy`, `reguser`, `regpsw` FROM `wiz_user` WHERE 1
    id = db.Column(Integer, unique=True, primary_key=True, autoincrement=True)
    invite_code = db.Column('invite_code')
    proxy = db.Column('proxy')
    reguser = db.Column('reguser')
    regcode = db.Column('regcode')
    regpsw = db.Column('regpsw')

    def __init__(self, invite_code, proxy, reguser, regcode, regpsw):
        self.invite_code = invite_code;
        self.proxy = proxy
        self.reguser = reguser
        self.regpsw = regpsw
        self.regcode = regcode


class Staff(db.Model):
    __tablename__ = 'DLS_STAFF_CHNL'
    #SELECT `staff_id`, `chnl_id`, `chnl_name` FROM `DLS_STAFF_CHNL` WHERE 1
    staffid = db.Column('staff_id', unique=True, primary_key=True)
    chnl_id = db.Column('chnl_id')
    chnl_name = db.Column('chnl_name')

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.staffid)

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

    def __init__(self, source=None, usercode=None, username=None, code=None):
        self.source = source
        self.usercode = usercode
        self.username = username
        self.code = code


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
