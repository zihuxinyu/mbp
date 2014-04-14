# coding: utf-8
from mbp.models import *
from sqlalchemy import  and_,or_,desc,asc
from DBLogic import AdoHelper

def getCompletedbyMissionId(MissionId):
    """
获取已经完成的资产清查条目数量
    :param MissionId:
    :return:
    """
    mm = mission_barcode.query \
        .filter(mission_barcode.missionid == MissionId) \
        .filter(mission_barcode.msgid != None) \
        .count()
    return mm
def getUnCompletedbyMissionId(MissionId):
    """
获取未完成资产条目数量
    :param MissionId:
    :return:
    """
    mm = mission_barcode.query \
        .filter(mission_barcode.missionid == MissionId) \
        .filter(mission_barcode.msgid == None) \
        .count()
    return mm
def getUnCompleteZCBQHbyMissionId(MissionId):
    return db.session.query(mission_barcode.barcode) \
        .filter(mission_barcode.missionid == MissionId) \
        .filter(mission_barcode.msgid == None)


def getCompleteZCBQHbyMissionId(MissionId):
    return mission_barcode.query \
        .filter(mission_barcode.missionid == MissionId) \
        .filter(mission_barcode.msgid != None).first().missionid


def getWrokingMissions():
    """
    获取当前进行中得核查任务

    """
    from DateLogic import  now
    mm=mission.query.filter(and_(mission.startdate<=now(),
                                 mission.enddate>=now())).all()
    return  mm


def getEndedMissions():
    """
    获取已经结束的核查任务

    """
    from DateLogic import now

    mm = mission.query.filter(mission.enddate <= now()).all()
    return mm

def getMissions():
    #data=AdoHelper().db().query("select * from mission")
    """
    获取所有的任务,并格式化为flask-admin的choice格式

    :return:
    """
    data=mission.query.all()
    return [(str(x.guid),x.missionname) for x in data]

def getMissionNameById(Id):
    """
    获取任务名称
    :param Id:
    :return:
    """
    sql="SELECT missionname FROM `mission` where guid={0}".format(Id)
    return AdoHelper().db().get(sql).missionname


def is_user_in_mission(user_code=None):
    """
    检查用户是否在核查人员列表中
    :param user_code:
    """
    sql = '''

     SELECT m.guid FROM mission m ,mission_user n where m.guid=n.missionid and m.startdate<=now() and m.enddate>=now()
     and n.user_code=%(user_code)s
        '''
    #print(sql)
    return len(AdoHelper().db().query(sql,user_code=user_code)) > 0
    #pass

def is_barcode_in_mission(user_code=None,barcode=None):
    """
    检查用户提交的barcode是否在任务之内
    :param user_code:
    :param barcode:
    :return:
    """
    sql='''
    SELECT * FROM mission_barcode x where missionid in (
 SELECT m.guid FROM mission m ,mission_user n where m.guid=n.missionid and m.startdate<=now() and m.enddate>=now()
 and n.user_code='{0}'
) and x.barcode='{1}'
    '''.format(user_code,barcode)
    #print(sql)
    return len(AdoHelper().db().query(sql))>0

def can_return(message):

    """
    检查是否需要反馈用户的信息
    检查此用户是否在任务期间
    :param message:
    """
    from mbp.Logic.WechatLogic import getUserBySource
    user=getUserBySource(message.source)
    if user:
        return  is_user_in_mission(user)
    else:
        return  False