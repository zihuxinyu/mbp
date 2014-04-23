# coding: utf-8
'''
文件作用:每天给过生日的人发短信
'''

from Library.DB import tornoracle3
from Library.datehelper import now, getCurDate
import time
import requests

def db():
    return tornoracle3.Connection(host='134.44.36.226',
                                  port='1521',
                                  database='ORCL',
                                  user='huiyuan',
                                  password='huiyuan')


def send():
    #短信模板
    smstmp = '''
        留不住的时光、年龄的递增赋予你的是成熟；而留得住的只有在这条温馨的短信上，涂抹得不标准的诗行，带去我们诚挚的祝福！生日当天您可以评此短信享受手机免费贴膜、配件5折、手机9折的超低优惠。中国电信滨州路营业厅全体工作人员祝您生日快乐！
        '''
    #发送短信的用户id
    senderid = '06dee4b6cedd4fd3a4d8480823678580'
    #短信接收地址
    url = 'http://www.laihuabao.com:8081/smstask/receive.aspx'

    #清除1年前的发送记录
    cleansql = '''DELETE FROM hy_birthsms  t WHERE trunc(sysdate - t.OPDATE)>360'''
    db().execute(cleansql)

    #插入当天生日的号码
    insertsql = '''
        INSERT INTO hy_birthsms h (phone,send)
    SELECT t.USER_MOBILE ,'0' as send from HY_USER t WHERE to_char( t.USER_BIRTH,'MMdd')=to_char(sysdate,'MMdd')
    AND t.USER_MOBILE NOT IN (SELECT h.PHONE FROM hy_birthsms h)
        '''
    db().execute(insertsql)

    #找出未发送的号码,send=0
    selectsql = "SELECT t.* from hy_birthsms t where send=0"
    list = db().query(selectsql)
    #print(list)
    phones = ['15605468613'] if list else []
    for x in list:
        print(x.PHONE)

        phones.append(x.PHONE)
        pass
    data = {'senderid': senderid,
            'target': ','.join(phones),
            'content': smstmp
    }
    if phones:
        r = requests.post(url, data=data)
        print(phones,r.text)
    else:
        print('No need to send birthday sms')

    #更新发送状态,send=1,opdate=sysdate

    updatesql = 'update hy_birthsms set opdate=sysdate , send=1 where opdate is null'
    db().execute(updatesql)

    print('birth sms send over')

if __name__ == "__main__":
    print()
    while True:
        h=int(now().split(' ')[1].split(':')[0])
        if h>8 and h<18:
            #规定发送时间
            print(h)
            send()
            pass
        time.sleep(60*60*3)