# # -*- coding: utf-8 -*-
# from scrapy.downloadermiddlewares.retry import RetryMiddleware
#
#
#
# class GetFailedUrl(RetryMiddleware):
#     def __init__(self, crawler):
#         super(GetFailedUrl, self).__init__(crawler.settings)
#         self.crawler = crawler
#         self.max_retry_times = crawler.settings.getint('RETRY_TIMES')
#         self.retry_http_codes = set(int(x) for x in crawler.settings.getlist('RETRY_HTTP_CODES'))
#         self.priority_adjust = crawler.settings.getint('RETRY_PRIORITY_ADJUST')
#
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         return cls(crawler)
#
#     def process_response(self, request, response, spider):
#         if response.status in self.retry_http_codes:
#         # 将爬取失败的URL存下来，你也可以存到别的存储
#             with open(str(spider.name) + ".txt", "a") as f:
#                 f.write(response.url + "\n")
#             return response
#         return response
#
#     def process_exception(self, request, exception, spider):
#     # 出现异常的处理
#         if isinstance(exception, self.EXCEPTIONS_TO_RETRY):
#             with open(str(spider.name) + ".txt", "a") as f:
#                 f.write(str(request) + "\n")
#             return None
