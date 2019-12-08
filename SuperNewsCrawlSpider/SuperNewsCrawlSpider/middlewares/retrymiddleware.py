# # -*- coding: utf-8 -*-
# import logging
# import time
# import random
# from scrapy.downloadermiddlewares.retry import RetryMiddleware
# from scrapy.utils.response import response_status_message
#
#
#
#
# class MyRetryMiddleware(RetryMiddleware):
#     logger = logging.getLogger(__name__)
#
#     def __init__(self, crawler):
#         super(MyRetryMiddleware, self).__init__(crawler.settings)
#         self.crawler = crawler
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         return cls(crawler)
#
#     def delete_proxy(self, proxy):
#         if proxy:
#             pass
#             # delete proxy from proxies pool
#
#
#     def process_response(self, request, response, spider):
#         if request.meta.get('dont_retry', False):
#             return response
#         if response.status in self.retry_http_codes:
#             reason = response_status_message(response.status)
#             # 删除该代理
#             self.delete_proxy(request.meta.get('proxy', False))
#             time.sleep(random.randint(3, 5))
#             self.logger.warning('返回值异常, 进行重试...')
#             return self._retry(request, reason, spider) or response
#         # return response
#
#         # if request.meta.get('dont_retry', False):
#         #     return response
#         # elif response.status == 429:
#         #     self.crawler.engine.pause()
#         #     time.sleep(60)  # If the rate limit is renewed in a minute, put 60 seconds, and so on.
#         #     self.crawler.engine.unpause()
#         #     reason = response_status_message(response.status)
#         #     return self._retry(request, reason, spider) or response
#         # elif response.status in self.retry_http_codes:
#         #     reason = response_status_message(response.status)
#         #     return self._retry(request, reason, spider) or response
#
#         return response
#
#
#     def process_exception(self, request, exception, spider):
#         if isinstance(exception, self.EXCEPTIONS_TO_RETRY) \
#                 and not request.meta.get('dont_retry', False):
#             # 删除该代理
#             self.delete_proxy(request.meta.get('proxy', False))
#             time.sleep(random.randint(3, 5))
#             self.logger.warning('连接异常, 进行重试...')
#
#             return self._retry(request, exception, spider)