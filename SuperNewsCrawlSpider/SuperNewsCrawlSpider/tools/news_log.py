# -*- coding: utf-8 -*-
import os
import logging

# 日志保存位置及日志文件名
logname="news_data"
# logpath = "/home/log/node_log"
logpath ="./"

# 日志系统
class logger_util(object):
    logsize = 1024 * 1024 * int(80000)
    lognum = int(3)
    logname = os.path.join(logpath, logname)
    logname = logname + ".log"

    log = logging.getLogger()
    formatter = logging.Formatter('[%(asctime)s][log.py][line:%(lineno)d][%(levelname)s] %(message)s',
                                  '%Y-%m-%d %H:%M:%S')

    handle = logging.FileHandler(logname)
    handle.setFormatter(formatter)

    console = logging.StreamHandler()
    console.setFormatter(formatter)
    # 给logger添加handler
    log.addHandler(handle)
    log.addHandler(console)
    log.setLevel(logging.INFO)

    @classmethod
    def info(cls, msg):
        cls.log.info(msg)
        return

    @classmethod
    def warning(cls, msg):
        cls.log.warning(msg)
        return

    @classmethod
    def error(cls, msg):
        cls.log.error(msg)
        return


# 获取日志错误信息
def log_message(code):
    httpcode_dict = {200: "200_SUCCESS",
                     301: "301_Redirect",
                     404: "404_NotFound",
                     403: "403_Forbidden",
                     6: "Title_AnalysisError",
                     7: "Content_AnalysisError",
                     8: "Time_AnalysisError",
                     9: "Author_AnalysisError",
                     10: "Other_AnalysisError",
                     11: "Save_Error"
                     }
    message = httpcode_dict.get(code)
    if message:
        return message
    else:
        return "Other_RequestError"


# 获取日志错误状态码
def log_status(code):
    httpcode_dict = {200: "1",
                     403: "2",
                     404: "3",
                     301: "4",
                     6: "6",
                     7: "7",
                     8: "8",
                     9: "9",
                     10: "10",
                     11: "11"
                     }
    message = httpcode_dict.get(code)
    if message:
        return message
    else:
        return "5"


# 日志信息
# def log_level(code, url):
#     error = "|" + es_index + "|" + get_time() + "|" + "0" + "|" + get_local_ip() + "|" + "0" + "|" + str(
#         url) + "|" + log_status(code) + "|" + log_message(code)
#     logger_util.error(error)

if __name__ == '__main__':
    pass