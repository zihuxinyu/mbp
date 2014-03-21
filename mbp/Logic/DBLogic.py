# coding: utf-8
import torndb
from config import DB_USER, DB_PSW, DB_HOST, DB_DATEBASE
def ado():
    return torndb.Connection(DB_HOST, DB_DATEBASE, DB_USER, DB_PSW)