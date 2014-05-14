# coding: utf-8
'''
miniui相关用法
'''
import json

from Library.jsonhelper import CJsonEncoder


def getData(sql,sqlwhere, pageSize, pageIndex,db):
    '''
    输出datagrid需要的格式
    pageIndex = int(request.form["pageIndex"]) if request.form["pageIndex"] else 0;
    pageSize = int( request.form["pageSize"]) if request.form["pageSize"] else 3;
    sql="select * from sqllist";
    sqlwhere=" 1";
    return getData(sql,sqlwhere,pageSize,pageIndex,AdoHelper().db())
    '''
    sqlcount = "select count(*) as count from ({intable} where {where}) xyz".format(intable=sql,where=sqlwhere);
    sqllimit = sql + " where  " + sqlwhere + " limit {0},{1}".format(pageSize * pageIndex, pageSize);

    count = db.get(sqlcount).count;
    list = db.query(sqllimit)

    data = {"total": count, 'data': list}

    return json.dumps(data, cls=CJsonEncoder)

def getGridData(entity,total=999,data=None):
    _columns_ = entity.__dict__['_columns_']
    data = [{x: getattr(row, x) for x in _columns_} for row in data]
    data = {"total": total, 'data': data}

    return json.dumps(data, cls=CJsonEncoder)