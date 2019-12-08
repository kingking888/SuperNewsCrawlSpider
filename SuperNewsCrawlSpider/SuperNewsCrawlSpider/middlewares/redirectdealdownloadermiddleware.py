# # -*- coding: utf-8 -*-
# from scrapy import signals
# from fake_useragent import UserAgent
# import random
# from scrapy.http import HtmlResponse
# import os
# import pickle
#
#
# class RedirectDealDownloaderMiddleware(object):
#     '''
#         处理知乎302重定向问题以及最初cookies传递问题
#     '''
#     def process_response(self, request, response, spider):
#         '''
#             deal with 302
#         '''
#         if response.status == 302 and 'signup' in response.url:
#             cookies = spider.get_cookies()
#             cookies_dict = {}
#             for cookie in cookies:
#                 cookies_dict[cookie["name"]] = cookie["value"]
#
#             headers = {
#                 'set-cookie': cookies_dict
#             }
#             return HtmlResponse(url=spider.browser.current_url, body=spider.browser.page_source,
#                                 encoding='utf8', request=request, headers=headers)
#         if 'signin' in response.url:
#             cookies = []
#             if os.path.exists(BASE_DIR+'/Zhihu/cookies/zhihu.cookies'):
#                 cookies = pickle.load(open(BASE_DIR+'/Zhihu/cookies/zhihu.cookies', 'rb'))
#
#             if not cookies:
#                 cookies = spider.get_cookies()
#
#             cookies_dict = {}
#             for cookie in cookies:
#                 cookies_dict[cookie["name"]] = cookie["value"]
#
#             headers = {
#                 'set-cookie': cookies_dict
#             }
#             return HtmlResponse(url=spider.browser.current_url, body=spider.browser.page_source,
#                                 encoding='utf8', request=request, headers=headers)
#         return response