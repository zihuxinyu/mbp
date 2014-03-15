__author__ = 'weibaohui'
# coding: utf-8
from mbp import db


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
        article = Article(
            title="点此查看" + x + "的资产详情",
            description="点此查看" + x + "的资产详情",
            img="http://d.hiphotos.baidu.com/baike/c0%3Dbaike150%2C5%2C5%2C150%2C50/sign"
                "=5800ef19a61ea8d39e2f7c56f6635b2b/38dbb6fd5266d01662dec68a972bd40734fae6cd7a891570.jpg",
            url='http://dyit.org/showzc/' + x
        )
        reply.add_article(article)
    return reply