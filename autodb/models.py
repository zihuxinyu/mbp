# -*- coding: utf8 -*-
import time

from autodb import db
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



class sqllist(db.Model):
    __tablename__ = 'sqllist'
    guid = db.Column(Integer, unique=True, primary_key=True, autoincrement=True)
    title = db.Column('title')
    sqlContent = db.Column('sqlContent')
    paras = db.Column('paras')
    frequency = db.Column('frequency')
    lastexec = db.Column('lastexec')
    nextexec = db.Column('nextexec')
    user_code = db.Column('user_code')
    opdate = db.Column('opdate')

    def __int__(self, title=None, sqlContent=None, paras=None, frequency=None, lastexec=None, nextexec=None,
                user_code=None, opdate=None):
        self.title = title
        self.sqlContent = sqlContent
        self.paras = paras
        self.frequency = frequency
        self.lastexec = lastexec
        self.nextexec = nextexec
        self.user_code = user_code
        self.opdate = opdate


class sqlresult(db.Model):
    __tablename__ = 'sqlresult'
    guid = db.Column(Integer, unique=True, primary_key=True, autoincrement=True)
    sguid = db.Column('sguid')
    sqlContent = db.Column('sqlContent')
    success = db.Column('success')
    message = db.Column('message')

    def __int__(self, sguid=None, sqlContent=None, success=None, message=None):
        self.sguid = sguid
        self.sqlContent = sqlContent
        self.success = success
        self.message = message