# coding: utf-8
from datetime import datetime
from datetime import date
from time import strftime, mktime,localtime
from time import strptime
from datetime import timedelta



def now(minutes=0):
    from datetime import datetime
    from datetime import timedelta


    now = datetime.now()
    aDay = timedelta( minutes=minutes)
    now = now + aDay
    return now.strftime('%Y-%m-%d %H:%M:%S')

def getOffsetDate(days=0):
    """
    获取时间差
    :param days:
    :return:datetime
    """
    now=datetime.now()
    aday=timedelta(days=days)
    return now+aday


def getLastMonth():
    from StringHelper import PadLeft
    import  time
    if time.localtime()[1] - 1:
        x= str(time.localtime()[0]) + PadLeft( str(time.localtime()[1] - 1),2,'0')
    else:
        x= str(time.localtime()[0]-1)+'12'

    return x


def getCurDate():
    """Return value of the date"""
    return date(datetime.now().year, datetime.now().month, datetime.now().day)


def getCurTime():
    """Return value of the datetime"""
    return datetime.now()


def converDateTimeToStr(cdate, format='%Y-%m-%d %H:%M:%S'):
    """
    Convert datetime to String
    cdata parameter must be the datetime or date of
    Return value of the date string format(%Y-%m-%d)
    """
    sdate = None
    try:
        sdate = cdate.strftime(format)
    except:
        raise ValueError
    return sdate


def converDateToDateTime(fdate):
    """
    Convert date to datetime
    fdate parameter must be the date of
    Return value of the datetime
    """
    return datetime(fdate.year, fdate.month, fdate.day, 0, 0, 0)


def converDateTimeToDate(fdate):
    """
    Convert datetime to date
    fdate parameter must be the datetime of
    Return value of the date
    """
    return date(fdate.year, fdate.month, fdate.day)


def converStrToDate(cstr):
    """
    Convert str to date
    cstr parameter must be the str of
    Return value of the date
    """
    fdate = None
    try:
        fdate = date(*strptime(cstr, '%Y-%m-%d')[0:3])
    except:
        raise ValueError
    return fdate


def converStrToDateTime(cstr):
    """
    Convert str to datetime
    cstr parameter must be the str of
    Return value of the datetime
    """
    fdate = None
    try:
        fdate = datetime(*strftime(cstr, '%Y-%m-%d %H:%M:%S')[0:6])
    except:
        raise ValueError
    return fdate


def getTheMonthDays(year, month):
    """the number of days a month"""
    if month + 1 > 12:
        month = 1
        year = year + 1
    else:
        month = month + 1

    return (datetime(year, month, 1) + timedelta(days=-1)).day


"""
#1.获得当前日期
curdate = getCurDate()
print '当前日期 :%s'%(curdate)

#2.获得当前时间
curtime = getCurTime()
print '当前时间  :%s'%(curtime)

#3.将当前日期转换为字符串
print '当前日期 :%s'%(converDateTimeToStr(curdate,'%Y-%m-%d'))

#4.将当前时间转换为字符串
print '当前时间:%s'%(converDateTimeToStr(curtime))

#5.将当前日期转换为时间
print '当前时间:%s' % (converDateToDateTime(curdate))

#6.将当前时间转换为日期
print '当前日期:%s' % (converDateTimeToDate(curtime))

#7.将字符串转换为日期
print '日期:%s' % (converStrToDate('2009-04-30'))

#8.将字符串转换为时间
print '时间:%s' % (converStrToDateTime('2009-04-30 23:59:59'))

#9.获得本月有多少天
print getTheMonthDays(curdate.year,curdate.month)
"""