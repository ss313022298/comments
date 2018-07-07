'''
Created on 2017年8月12日

@author: zhangqingwei
'''

def format_time(timestamp):
    second = int(float(timestamp))
    if second <= 0:
        return ''
    d = int(second / (3600 * 24))
    h = int(second % (3600 * 24) / 3600)
    m = int(second % 3600 / 60)
    s = second % 3600 % 60
    day, hour, minute, second = '', '', '', ''
    if d != 0:
        day = '%s天' % str(d)
    if h != 0:
        hour = '%s小时' % str(h)
    if m != 0:
        minute = '%s分' % str(m)
    if s != 0:
        second = '%s秒' % str(s)
    time_result = '%s%s%s%s' % (day, hour, minute, second)
    return time_result
    