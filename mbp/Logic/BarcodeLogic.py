# coding: utf-8
from mbp import db
from mbp.models import zczb
from sqlalchemy import and_, desc
from mbp.models import BarcodeList, mission_barcode
from  WechatLogic import getUserBySource
from Library.datehelper import now
from mbp.Logic.MissionLogic import is_barcode_in_mission
def ChkUnicomBarcode(code):
    """
    验证是否联通公司资产编号
    :rtype : Boolean
    :param code:条形码
    """
    code = (code).strip()
    if code.startswith('123706-') and len(code) == 15:
        return True
    elif len(code)==8:
        return  True
    else:
        return False


def GetUnicomBarcode(code):
    """

    :param code:扫描进来的资产编号
    :return: 返回符号联通资产编号的列表
    """
    #统一加上一个分号,方便后面进行列表操作
    code += ';'

    xx = code.split(';')
    yy = [x for x in xx if ChkUnicomBarcode(x)]
    yy = ['123706-'+x if len(x)==8 else x  for x in yy]
    return yy


def SaveBarcode(barcodelist, message, type='input'):
    """
    将识别的二维码保存下来
    :param barcodelist:联通资产码列表
    :param type:
    :param message:
    """

    for x in barcodelist:

        uu=getUserBySource(message.source)
        if uu:
            if is_barcode_in_mission(user_code=uu,barcode=x):
            #如果此用户提交的时任务内的资产标签,那么保存下来
                pp=getPortalUser(uu)
                bb = BarcodeList(source=message.source, barcode=x,
                             type=type, msgid=message.id,
                             user_code=uu,opdate=now(),
                             topdpt=pp.topdpt)
                db.session.add(bb)
                mb=mission_barcode.query.filter(and_(mission_barcode.barcode==x,  mission_barcode.msgid==None) )
                if mb.first():
                    #只更新没有扫描到得二维码,填了msgid证明已经查过
                    mb.update({mission_barcode.msgid:message.id})

    db.session.commit()


def ShowBarDetail(barcodelist, message):
    """
    查看资产详情页面
    :param barcodelist:联通资产码列表
    :return:
    """
    if len(barcodelist) > 9:
        barcodelist = barcodelist[0:10]
    from werobot.reply import ArticlesReply, Article, create_reply

    reply = ArticlesReply(message=message)
    for x in barcodelist:

        zz=ShowBarSmart(x)

        article = Article(
            title="点此查看" + x + "的资产详情",
            description=zz if  zz else "尚未收录",
            img="http://d.hiphotos.baidu.com/baike/c0%3Dbaike150%2C5%2C5%2C150%2C50/sign"
                "=5800ef19a61ea8d39e2f7c56f6635b2b/38dbb6fd5266d01662dec68a972bd40734fae6cd7a891570.jpg",
            url='http://dyit.org/showzc/?zcbh=' + x+'&msgid='+str(message.id)
        )
        reply.add_article(article)
    return reply


def ShowBarSmart(barcode):
    """
    获取简介形式的资产标签说明
    :param barcode:
    """
    zz = zczb.query.filter(zczb.zcbqh == barcode).first()
    znum= len( getChild(barcode))
    if zz:
        if znum>0:
            return '名称:{0}\r\n规格:{1}\r\n物理位置:{7}\r\n启用日期:{2}\r\n下电标识:{5}\r\n报废标识:{3}\r\n生命周期:{6}\r\n子资产数:{4}\r\n'.format(zz.swmc,zz.ggxh,zz.qyrq.replace('00:00:00',''),zz.bfbz,znum,zz.xdbz,zz.sbsmzj,zz.jjhlh)
        else:
            return '名称:{0}\r\n规格:{1}\r\n物理位置:{6}\r\n启用日期:{2}\r\n下电标识:{4}\r\n报废标识:{3}\r\n生命周期:{5}'.format(zz.swmc,
                                                                                                          zz.ggxh,
                                                                                                          zz.qyrq.replace('00:00:00',
                                                                                                              ''),
                                                                                                          zz.bfbz,
                                                                                                          zz.xdbz,
                                                                                                          zz.sbsmzj,
                                                                                                          zz.jjhlh)
    else:
        return None
def getChild(barcode):
    """
    获取子资产数目
    :param barcode:
    :return:
    """
    return zczb.query.filter(zczb.fzcbqh == barcode).all()
def getPortalUser(user_code=None):
    """
    通过user_code获取门户信息,包括手机号,组织架构等
    :param user_code:
    :return:
    """
    from mbp.models import portal_user
    pp=portal_user.query.filter(portal_user.user_code==user_code).first()
    return pp