# import time
# import os
#
#
# """
# ʵ��ÿ��һ��ʱ������һ������
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
#         print('�ѵȴ�%s���ӣ�������һ���Ѽ����ݻ���%s����......'%(remindCount*remindTime,(sleepTime/remindTime-(remindCount))*remindTime))