# coding: utf-8
'''
miniui相关用法
'''
import json
import itertools
from Library.flaskhelper import getargs
from pony.orm import *
from Library.jsonhelper import CJsonEncoder


class Row(dict):
    """A dict that allows for object-like property access syntax."""

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)


def getGridData(entity=None, total=0, data=None):
    '''
    获得miniui显示需要的表格json,自动获取排序,分页信息
    多表联合查询时必须要把排序放在方法外实现
    entity单表时可以不指定total,方法自动count(*)计算
    :param entity: pony实体
    :param total:总数
    :param data:数据集
    data= select((p.title,x.sguid,p.guid,p.nextexec) for p in sqllist for x in sqlresult if  p.guid==x.sguid)
    '''
    pageIndex = int(getargs("pageIndex", 0))
    pageSize = int(getargs("pageSize", 0))
    sortField = getargs('sortField')
    sortOrder = getargs('sortOrder')
    if entity:
        #single entity
        #取主键count 性能更好,如果没有指定就count(*)
        total=data.count() if not total else total

        #带排序字段
        if sortField:
            if str(sortOrder).lower() == "asc":
                data = data.order_by(getattr(entity, sortField))
            else:
                data = data.order_by(desc(getattr(entity, sortField)))
        #带分页
        if pageIndex or pageSize:
            data = data.limit(pageSize, pageSize * pageIndex)

        _columns_ = entity.__dict__['_columns_']
        data = [{x: getattr(row, x) for x in _columns_} for row in data]


    else:
        #muiltpe table
        #带分页
        if pageIndex or pageSize:
            # 转换为QueryObject 获得_col_names
            data = data.limit(pageSize, pageSize * pageIndex)

        data = [Row(itertools.izip([x.split('.')[1] for x in data._col_names], row)) for row in data]


    data = {"total": total, 'data': data}
    return json.dumps(data, cls=CJsonEncoder)


def getGridDataOnly(entity=None, total=999, data=None):
    '''
    只对传入的Data进行组装,适合自行控制分页,排序的情况,多表情况必须先执行data.limit(n),转换为queryobject
    :param entity: pony实体
    :param total:总数
    :param data:数据集
    '''
    if entity:
        # single entity
        _columns_ = entity.__dict__['_columns_']
        data = [{x: getattr(row, x) for x in _columns_} for row in data]

    else:
        # muiltpe table
        data = [Row(itertools.izip([x.split('.')[1] for x in data._col_names], row)) for row in data]

    data = {"total": total, 'data': data}

    return json.dumps(data, cls=CJsonEncoder)

def saveData(entity, data):
    '''
    保存json格式的数据,_state:表明CURD状态
    '''
    for d in data:
        d = Row(d)
        _columns_ = entity.__dict__['_columns_']
        _pk_columns_ = entity.__dict__['_pk_columns_']
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