__author__ = 'weibaohui'
# coding: utf-8
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