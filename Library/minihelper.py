# coding: utf-8
'''
miniui相关用法
'''
import json

from Library.jsonhelper import CJsonEncoder


class Row(dict):
    """A dict that allows for object-like property access syntax."""

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

def getGridData(entity,total=999,data=None):
    _columns_ = entity.__dict__['_columns_']
    data = [{x: getattr(row, x) for x in _columns_} for row in data]
    data = {"total": total, 'data': data}

    return json.dumps(data, cls=CJsonEncoder)
