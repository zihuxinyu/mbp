# coding: utf-8
'''
miniui相关用法
'''
import json

from Library.jsonhelper import CJsonEncoder





def getGridData(entity,total=999,data=None):
    _columns_ = entity.__dict__['_columns_']
    data = [{x: getattr(row, x) for x in _columns_} for row in data]
    data = {"total": total, 'data': data}

    return json.dumps(data, cls=CJsonEncoder)