# import time
# import os
#
#
# """
# 实现每隔一段时间运行一个命令
# """
#
#
# while True:
#     os.system("scrapy crawlall")
#     remindTime = 5
#     remindCount = 0
#     sleepTime = 60
#     while remindCount * remindTime < sleepTime:
#         time.sleep(remindTime*60)
#         remindCount = remindCount + 1
#         print('已等待%s分钟，距离下一次搜集数据还有%s分钟......'%(remindCount*remindTime,(sleepTime/remindTime-(remindCount))*remindTime))