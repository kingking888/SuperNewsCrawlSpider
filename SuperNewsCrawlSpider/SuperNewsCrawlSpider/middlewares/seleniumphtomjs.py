# # -*- coding: utf-8 -*-
#
# # Define here the models for your spider middleware
# #
# # See documentation in:
# # http://doc.scrapy.org/en/latest/topics/spider-middleware.html
#
# from selenium import webdriver
# import time
# # from scrapy.downloadermiddlewares.stats import DownloaderStats
# from scrapy.http import Request, FormRequest, HtmlResponse
#
# #headers
# cap = webdriver.DesiredCapabilities.PHANTOMJS
# cap["phantomjs.page.settings.resourceTimeout"] = 1000
# cap["phantomjs.page.settings.loadImages"] = False
# cap["phantomjs.page.settings.disk-cache"] = True
# cap["phantomjs.page.customHeaders.Cookie"] = 'aliyungf_tc=AQAAAIplnShTMAQAebbT3lEVm4rc3txx; '
# cap["phantomjs.page.settings.userAgent"] = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
# cap['phantomjs.page.settings.connection'] = 'keep-alive'
# cap['phantomjs.page.settings.host'] = 'xueqiu.com'
#
#
# #定义在外部 防止多次实例phantomjs
# global  driver
# #service_args=['..'] 具备访问加密请求https的功能
# driver = webdriver.PhantomJS(service_args=['--ssl-protocol=any'],executable_path="F:\wwwroot\python_module/phantomjs",desired_capabilities=cap)
#
# class WooghtDownloadMiddleware(object):
#
#     def process_request(self, request, spider):
#         global driver
#         js = "var q=document.body.scrollTop=2000"
#         url=request.url;
#         if(spider.name=='xueqiu2'):                                                         #特定spider允许
#             #雪球首页
#             driver.get(url)
#             time.sleep(2)
#             driver.execute_script(js)                                                       #运行JS 模拟滑动到底部
#             time.sleep(2)
#             driver.execute_script("var a=document.body.scrollTop=5000")                     #第二次下拉
#             print('delay 2S----------------------------------------------------\n')
#             body = driver.page_source                                                       #获取素有内容
#             # driver.quit()                                                                 #关闭浏览器,只能关闭一次 如果每次调用都关闭,会遭到反爬虫
#             response = HtmlResponse(body=body, encoding='utf-8',request=request,url=str(url))   #返回response数据供spider paser处理
#             response.meta['web_title'] = driver.title                                       #传递其他参数供spider使用
#             return response
#         elif(spider.name=='Sseinfo_shede'):
#             #上证E互动-沱牌舍得问答
#             driver.get(url)
#             print('\n-=-=-=-=-=-=-=-'+url+'=-=-=-=-=-=-=-=-=-=-\n')
#             time.sleep(1)
#             driver.execute_script(js)
#             arr = [1,2,3,4]
#             for i in arr:
#                 time.sleep(1)
#                 js = "var a=document.body.scrollTop="+str(i*3000)
#                 driver.execute_script(js)
#                 if 'gushi' in url:                                                 #如果是首页 点击下一页获取更多
#                     button_id = driver.find_element_by_id('divMore')               #找到按钮元素
#                     button_id.click()                                              #点击按钮
#             body = driver.page_source
#             print(driver.title,'=-=-=-=-=sseinfo-=-=-=-=-=-')
#             return HtmlResponse(body=body, encoding='utf-8',request=request,url=str(url))
#         elif(spider.name=='Xueqiutoutiao'):
#             driver.get(url)
#             print('\n-=-=-=-=-=-=-=-'+url+'=-=-=-=-=-=-=-=-=-=-\n')
#             time.sleep(1)
#             driver.execute_script(js)
#             if(len(url)<20):
#                 arr = [1,2,3]
#                 for i in arr:
#                     time.sleep(1)
#                     js = "var a=document.body.scrollTop="+str(i*3000)
#                     driver.execute_script(js)
#             body = driver.page_source
#             print(driver.title,'=-=-=-=-=Xueqiutoutiao-=-=-=-=-=-')
#             return HtmlResponse(body=body, encoding='utf-8',request=request,url=str(url))
#
#
#     #关闭浏览器
#     def spider_closed(self, spider, reason):
#         global driver
#         print ('close driver......')
#         driver.close()