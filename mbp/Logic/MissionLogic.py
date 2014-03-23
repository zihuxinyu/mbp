# coding: utf-8
from mbp.models import *
from sqlalchemy import  and_,or_,desc,asc

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
    return db.session.query(mission_barcode.barcode) \
        .filter(mission_barcode.missionid == MissionId) \
        .filter(mission_barcode.msgid != None)


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
