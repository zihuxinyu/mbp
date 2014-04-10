# -*- coding: utf8 -*-
import time

from mbp import db
from sqlalchemy import Integer

ROLE_USER = 0
ROLE_ADMIN = 1


class portal_user(db.Model):
    guid = db.Column(Integer, unique=True, primary_key=True, autoincrement=True)
    user_code = db.Column('user_code')
    user_name = db.Column('user_name')
    user_mobile = db.Column('user_mobile')
    dpt_name = db.Column('dpt_name')
    topdpt = db.Column('topdpt')
    manager = db.Column('manager')
    msg = db.Column('msg')
    msgexpdate = db.Column('msgexpdate')

    def __int__(self, user_code=None, user_name=None, user_mobile=None, dpt_name=None, topdpt=None, manager=None,
                msg=None,
                msgexpdate=None):
        self.user_code = user_code
        self.user_name = user_name
        self.user_mobile = user_mobile
        self.dpt_name = dpt_name
        self.topdpt = topdpt
        self.manager = manager
        self.msg = msg
        self.msgexpdate = msgexpdate

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.user_code)


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
    checked = db.Column('checked')

    def __init__(self, source=None, usercode=None, username=None, code=None, checked=0):
        self.source = source
        self.usercode = usercode
        self.username = username
        self.code = code
        self.checked = checked


class BarcodeList(db.Model):
    __tablename__ = 'barcodelist'
    guid = db.Column(Integer, unique=True, primary_key=True, autoincrement=True)
    barcode = db.Column('barcode')
    source = db.Column('source')
    user_code = db.Column('user_code')
    msgid = db.Column('msgid')
    topdpt= db.Column('topdpt')
    opdate = db.Column('opdate')
    type = db.Column('type')
    ztbz = db.Column('ztbz')
    ztbz1 = db.Column('ztbz1')
    ztbz2 = db.Column('ztbz2')
    ztbz3 = db.Column('ztbz3')
    ztbz4 = db.Column('ztbz4')
    wlwz = db.Column('wlwz')

    def __int__(self, barcode=None, source=None, user_code=None, topdpt=None, msgid=None, opdate=None, type=None,
                ztbz=None, ztbz1=None, ztbz2=None, ztbz3=None, ztbz4=None, wlwz=None):
        self.barcode = barcode
        self.source = source
        self.user_code = user_code
        self.topdpt = topdpt
        self.msgid = msgid
        self.opdate = opdate
        self.type = type
        self.ztbz = ztbz
        self.ztbz1 = ztbz1
        self.ztbz2 = ztbz2
        self.ztbz3 = ztbz3
        self.ztbz4 = ztbz4
        self.wlwz = wlwz


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


class zczb(db.Model):
    guid = db.Column(Integer, unique=True, primary_key=True, autoincrement=True)
    zdmc = db.Column('zdmc')
    sf = db.Column('sf')
    ds = db.Column('ds')
    zcly = db.Column('zcly')
    zcbqh = db.Column('zcbqh')
    yzcbqh = db.Column('yzcbqh')
    sblx = db.Column('sblx')
    sbjb = db.Column('sbjb')
    yzcmc = db.Column('yzcmc')
    swmc = db.Column('swmc')
    swzt = db.Column('swzt')
    swfl = db.Column('swfl')
    gsbh = db.Column('gsbh')
    zczbbh = db.Column('zczbbh')
    gkglzyx = db.Column('gkglzyx')
    zygkglbm = db.Column('zygkglbm')
    zczyglzrrygbh = db.Column('zczyglzrrygbh')
    zgzyglzrrxm = db.Column('zgzyglzrrxm')
    qcbzyx = db.Column('qcbzyx')
    dlswbz = db.Column('dlswbz')
    fzcbqh = db.Column('fzcbqh')
    yyly = db.Column('yyly')
    zcml = db.Column('zcml')
    zchszy = db.Column('zchszy')
    zcgjzms = db.Column('zcgjzms')
    zcgjz = db.Column('zcgjz')
    xtzylx = db.Column('xtzylx')
    gysmc = db.Column('gysmc')
    sccsmc = db.Column('sccsmc')
    yggxh = db.Column('yggxh')
    ggxh = db.Column('ggxh')
    xlh = db.Column('xlh')
    zcsl = db.Column('zcsl')
    zcsldw = db.Column('zcsldw')
    fzsl = db.Column('fzsl')
    fujldw = db.Column('fujldw')
    gmrq = db.Column('gmrq')
    qyrq = db.Column('qyrq')
    syys = db.Column('syys')
    zbksrq = db.Column('zbksrq')
    zbjzrq = db.Column('zbjzrq')
    xmbh = db.Column('xmbh')
    xmmc = db.Column('xmmc')
    xmfl = db.Column('xmfl')
    sfkr = db.Column('sfkr')
    zrbmbm = db.Column('zrbmbm')
    zrbmmc = db.Column('zrbmmc')
    zrrygbh = db.Column('zrrygbh')
    zrrxm = db.Column('zrrxm')
    bgryxdz = db.Column('bgryxdz')
    faddbm = db.Column('faddbm')
    faddms = db.Column('faddms')
    bzdz = db.Column('bzdz')
    zcyz = db.Column('zcyz')
    zcjz = db.Column('zcjz')
    whfs = db.Column('whfs')
    whbm = db.Column('whbm')
    whzrrygbh = db.Column('whzrrygbh')
    whzrrygxm = db.Column('whzrrygxm')
    whryxdz = db.Column('whryxdz')
    sfxcgwb = db.Column('sfxcgwb')
    zcgs = db.Column('zcgs')
    zypzms = db.Column('zypzms')
    xyxt = db.Column('xyxt')
    sxsj = db.Column('sxsj')
    xxsj = db.Column('xxsj')
    edgl = db.Column('edgl')
    dydwgxtzdzjmc = db.Column('dydwgxtzdzjmc')
    sbszjfsx = db.Column('sbszjfsx')
    jjhlh = db.Column('jjhlh')
    qsu = db.Column('qsu')
    gd = db.Column('gd')
    oslxjbb = db.Column('oslxjbb')
    bdxx = db.Column('bdxx')
    wxmacdz = db.Column('wxmacdz')
    yxmacdz = db.Column('yxmacdz')
    sbhostname = db.Column('sbhostname')
    sboid = db.Column('sboid')
    sbdescription = db.Column('sbdescription')
    ipxx = db.Column('ipxx')
    slwlsb = db.Column('slwlsb')
    sbcj = db.Column('sbcj')
    jjlx = db.Column('jjlx')
    zjlx = db.Column('zjlx')
    zjsl = db.Column('zjsl')
    jjdsmlx = db.Column('jjdsmlx')
    swms = db.Column('swms')
    zdyt = db.Column('zdyt')
    zzbz = db.Column('zzbz')
    kzlybz = db.Column('kzlybz')
    xdbz = db.Column('xdbz')
    ygcbhjmc = db.Column('ygcbhjmc')
    ysr = db.Column('ysr')
    fsssjfj = db.Column('fsssjfj')
    bz = db.Column('bz')
    bfbz = db.Column('bfbz')
    bz1 = db.Column('bz1')
    bz2 = db.Column('bz2')
    bz3 = db.Column('bz3')
    bz4 = db.Column('bz4')
    bz5 = db.Column('bz5')
    sbsmzj = db.Column('sbsmzj')
    sjlyfl = db.Column('sjlyfl')

    def __int__(self, zdmc=None, sf=None, ds=None, zcly=None, zcbqh=None, yzcbqh=None, sblx=None, sbjb=None, yzcmc=None,
                swmc=None, swzt=None, swfl=None, gsbh=None, zczbbh=None, gkglzyx=None, zygkglbm=None,
                zczyglzrrygbh=None, zgzyglzrrxm=None, qcbzyx=None, dlswbz=None, fzcbqh=None, yyly=None, zcml=None,
                zchszy=None, zcgjzms=None, zcgjz=None, xtzylx=None, gysmc=None, sccsmc=None, yggxh=None, ggxh=None,
                xlh=None, zcsl=None, zcsldw=None, fzsl=None, fujldw=None, gmrq=None, qyrq=None, syys=None, zbksrq=None,
                zbjzrq=None, xmbh=None, xmmc=None, xmfl=None, sfkr=None, zrbmbm=None, zrbmmc=None, zrrygbh=None,
                zrrxm=None, bgryxdz=None, faddbm=None, faddms=None, bzdz=None, zcyz=None, zcjz=None, whfs=None,
                whbm=None, whzrrygbh=None, whzrrygxm=None, whryxdz=None, sfxcgwb=None, zcgs=None, zypzms=None,
                xyxt=None, sxsj=None, xxsj=None, edgl=None, dydwgxtzdzjmc=None, sbszjfsx=None, jjhlh=None, qsu=None,
                gd=None, oslxjbb=None, bdxx=None, wxmacdz=None, yxmacdz=None, sbhostname=None, sboid=None,
                sbdescription=None, ipxx=None, slwlsb=None, sbcj=None, jjlx=None, zjlx=None, zjsl=None, jjdsmlx=None,
                swms=None, zdyt=None, zzbz=None, kzlybz=None, xdbz=None, ygcbhjmc=None, ysr=None, fsssjfj=None, bz=None,
                bfbz=None, bz1=None, bz2=None, bz3=None, bz4=None, bz5=None, sbsmzj=None, sjlyfl=None):
        self.zdmc = zdmc
        self.sf = sf
        self.ds = ds
        self.zcly = zcly
        self.zcbqh = zcbqh
        self.yzcbqh = yzcbqh
        self.sblx = sblx
        self.sbjb = sbjb
        self.yzcmc = yzcmc
        self.swmc = swmc
        self.swzt = swzt
        self.swfl = swfl
        self.gsbh = gsbh
        self.zczbbh = zczbbh
        self.gkglzyx = gkglzyx
        self.zygkglbm = zygkglbm
        self.zczyglzrrygbh = zczyglzrrygbh
        self.zgzyglzrrxm = zgzyglzrrxm
        self.qcbzyx = qcbzyx
        self.dlswbz = dlswbz
        self.fzcbqh = fzcbqh
        self.yyly = yyly
        self.zcml = zcml
        self.zchszy = zchszy
        self.zcgjzms = zcgjzms
        self.zcgjz = zcgjz
        self.xtzylx = xtzylx
        self.gysmc = gysmc
        self.sccsmc = sccsmc
        self.yggxh = yggxh
        self.ggxh = ggxh
        self.xlh = xlh
        self.zcsl = zcsl
        self.zcsldw = zcsldw
        self.fzsl = fzsl
        self.fujldw = fujldw
        self.gmrq = gmrq
        self.qyrq = qyrq
        self.syys = syys
        self.zbksrq = zbksrq
        self.zbjzrq = zbjzrq
        self.xmbh = xmbh
        self.xmmc = xmmc
        self.xmfl = xmfl
        self.sfkr = sfkr
        self.zrbmbm = zrbmbm
        self.zrbmmc = zrbmmc
        self.zrrygbh = zrrygbh
        self.zrrxm = zrrxm
        self.bgryxdz = bgryxdz
        self.faddbm = faddbm
        self.faddms = faddms
        self.bzdz = bzdz
        self.zcyz = zcyz
        self.zcjz = zcjz
        self.whfs = whfs
        self.whbm = whbm
        self.whzrrygbh = whzrrygbh
        self.whzrrygxm = whzrrygxm
        self.whryxdz = whryxdz
        self.sfxcgwb = sfxcgwb
        self.zcgs = zcgs
        self.zypzms = zypzms
        self.xyxt = xyxt
        self.sxsj = sxsj
        self.xxsj = xxsj
        self.edgl = edgl
        self.dydwgxtzdzjmc = dydwgxtzdzjmc
        self.sbszjfsx = sbszjfsx
        self.jjhlh = jjhlh
        self.qsu = qsu
        self.gd = gd
        self.oslxjbb = oslxjbb
        self.bdxx = bdxx
        self.wxmacdz = wxmacdz
        self.yxmacdz = yxmacdz
        self.sbhostname = sbhostname
        self.sboid = sboid
        self.sbdescription = sbdescription
        self.ipxx = ipxx
        self.slwlsb = slwlsb
        self.sbcj = sbcj
        self.jjlx = jjlx
        self.zjlx = zjlx
        self.zjsl = zjsl
        self.jjdsmlx = jjdsmlx
        self.swms = swms
        self.zdyt = zdyt
        self.zzbz = zzbz
        self.kzlybz = kzlybz
        self.xdbz = xdbz
        self.ygcbhjmc = ygcbhjmc
        self.ysr = ysr
        self.fsssjfj = fsssjfj
        self.bz = bz
        self.bfbz = bfbz
        self.bz1 = bz1
        self.bz2 = bz2
        self.bz3 = bz3
        self.bz4 = bz4
        self.bz5 = bz5
        self.sbsmzj = sbsmzj
        self.sjlyfl = sjlyfl


class mission_barcode(db.Model):
    '''
    定义任务与资产标签号关系
    '''
    __tablename__ = 'mission_barcode'
    guid = db.Column(Integer, unique=True, primary_key=True, autoincrement=True)
    missionid = db.Column('missionid', db.String(10))
    barcode = db.Column('barcode', db.String(100))
    msgid = db.Column('msgid')

    def __int__(self, missionid=None, barcode=None, msgid=None):
        self.missionid = missionid
        self.barcode = barcode
        self.msgid = msgid


class mission(db.Model):
    '''
    定义了任务
    '''
    __tablename__ = 'mission'
    guid = db.Column(Integer, unique=True, primary_key=True, autoincrement=True)
    missionname = db.Column('missionname', db.String(100))
    startdate = db.Column('startdate',db.DATE)
    enddate = db.Column('enddate',db.DATE)

    def __int__(self, missionname=None, startdate=None, enddate=None):
        self.missionname = missionname
        self.startdate = startdate
        self.enddate = enddate


class mission_user(db.Model):
    '''
    定义了任务与用户关系
    '''
    __tablename__ = 'mission_user'
    guid = db.Column(Integer, unique=True, primary_key=True, autoincrement=True)
    missionid = db.Column('missionid',db.String(10))
    user_code = db.Column('user_code',db.String(30))

    def __int__(self, missionid=None, user_code=None):
        self.missionid = missionid
        self.user_code = user_code


class usergroup(db.Model):
    '''
    定义用户角色关系表
    '''
    __tablename__ = 'usergroup'
    guid = db.Column(Integer, unique=True, primary_key=True, autoincrement=True)
    user_code = db.Column('user_code',db.String(50))
    groupid = db.Column('groupid',db.String(50))

    def __int__(self, user_code=None, groupid=None):
        self.user_code = user_code
        self.groupid = groupid