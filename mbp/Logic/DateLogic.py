# coding: utf-8
def now():
    import time
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))