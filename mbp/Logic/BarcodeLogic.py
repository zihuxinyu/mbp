# coding: utf-8
from mbp import db
from mbp.models import zczb

def ChkUnicomBarcode(code):
    """
    验证是否联通公司资产编号
    :rtype : Boolean
    :param code:条形码
    """
    code = (code).strip()
    if code.startswith('123706-') and len(code) == 15:
        return True
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
    return yy


def SaveBarcode(barcodelist, message, type='input'):
    """
    将识别的二维码保存下来
    :param barcodelist:联通资产码列表
    :param type:
    :param message:
    """

    for x in barcodelist:
        from mbp.models import BarcodeList

        bb = BarcodeList(source=message.source, barcode=x, type=type, msgid=message.id)
        db.session.add(bb)
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
            url='http://dyit.org/showzc/' + x
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
            return '名称:{0}\r\n规格:{1}\r\n启用日期:{2}\r\n报废标识:{3}\r\n子资产数:{4}'.format(zz.swmc,zz.ggxh,zz.qyrq,zz.bfbz,znum)
        else:
            return '名称:{0}\r\n规格:{1}\r\n启用日期:{2}\r\n报废标识:{3}'.format(zz.swmc, zz.ggxh, zz.qyrq, zz.bfbz)
    else:
        return None
def getChild(barcode):
    """
    获取子资产数目
    :param barcode:
    :return:
    """
    return zczb.query.filter(zczb.fzcbqh == barcode).all()