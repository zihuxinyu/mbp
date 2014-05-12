# coding: utf-8
'''
解决json TypeError: datetime.datetime(2012, 12, 12, 15, 47, 15) is not JSON serializable

json.dumps(datalist, cls=CJsonEncoder)
'''
import json
from datetime import datetime
class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')

        elif isinstance(obj, datetime.date):

            return obj.strftime('%Y-%m-%d')

        else:

            return json.JSONEncoder.default(self, obj)