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
    '''
    获得miniui显示需要的表格json
    '''
    _columns_ = entity.__dict__['_columns_']
    data = [{x: getattr(row, x) for x in _columns_} for row in data]
    data = {"total": total, 'data': data}

    return json.dumps(data, cls=CJsonEncoder)

def saveData(entity,data):
    '''
    保存json格式的数据,_state:表明CURD状态
    '''
    for d in data:
        d = Row(d)
        _columns_ = entity.__dict__['_columns_']
        _pk_columns_ = entity.__dict__['_pk_columns_']
        print(type(_pk_columns_))
        if d._state == 'modified':  #修改
            guid = {c: d[c] for c in _pk_columns_}
            changed = {c: d[c] for c in _columns_ if c in d and c not in _pk_columns_}
            entity.get(**guid).set(**changed)

        elif d._state == 'added':
            changed = {c: d[c] for c in _columns_ if c in d and c not in _pk_columns_}
            entity(**changed)
        elif d._state == 'removed':
            guid = {c: d[c] for c in _pk_columns_}
            entity.get(**guid).delete()