# encoding: utf-8
import time
import datetime



class GetTime(object):
    def __init__(self):
        pass
    # 获取当前时间
    def get_time(self):
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


    # 获取当前时间的前一个小时时间
    def get_first_hour(self):
        tim = datetime.datetime.now()
        # datetime.timedelta(days=0, seconds=0, microseconds=0)#毫秒, milliseconds=0, minutes=0, hours=0, weeks=0)
        first_hour = (tim + datetime.timedelta(hours=-1)).strftime("%Y-%m-%d %H")
        return first_hour


    # 获取当前时间的前一天的时间
    def get_yesterday_date(self):
        tim = datetime.datetime.now()
        yesterday_date = (tim + datetime.timedelta(days=-1)).strftime("%Y-%m-%d")
        return yesterday_date

if __name__ == '__main__':
    pass