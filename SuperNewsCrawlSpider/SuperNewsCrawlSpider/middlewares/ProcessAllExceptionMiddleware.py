from twisted.internet import defer
from twisted.internet.error import TimeoutError, DNSLookupError, \
    ConnectionRefusedError, ConnectionDone, ConnectError, \
    ConnectionLost, TCPTimedOutError
from scrapy.http import HtmlResponse
from twisted.web.client import ResponseFailed
from scrapy.core.downloader.handlers.http11 import TunnelError



class ProcessAllExceptionMiddleware(object):
    ALL_EXCEPTIONS = (defer.TimeoutError, TimeoutError, DNSLookupError,
                      ConnectionRefusedError, ConnectionDone, ConnectError,
                      ConnectionLost, TCPTimedOutError, ResponseFailed,
                      IOError, TunnelError)

    def process_response(self, request, response, spider):
        # ����״̬��Ϊ40x/50x��response
        if str(response.status).startswith('4') or str(response.status).startswith('5'):
            # �����װ��ֱ�ӷ���response��spider�����и���url==''������response
            response = HtmlResponse(url='')
            return response
        # ����״̬�벻����
        return response

    def process_exception(self, request, exception, spider):
        # ���񼸺����е��쳣
        if isinstance(exception, self.ALL_EXCEPTIONS):
            # ����־�д�ӡ�쳣����
            print('Got exception: %s' % (exception))
            # �����װһ��response�����ظ�spider
            response = HtmlResponse(url='exception')
            return response
        # ��ӡ��δ���񵽵��쳣
        print('not contained exception: %s' % exception)

#     def process_spider_input(self, response, spider):
#         if 200 <= response.status < 300:  # common case
#             return
#         meta = response.meta
#         if 'handle_httpstatus_all' in meta:
#             return
#         if 'handle_httpstatus_list' in meta:
#             allowed_statuses = meta['handle_httpstatus_list']
#         elif self.handle_httpstatus_all:
#             return
#         else:
#             allowed_statuses = getattr(spider, 'handle_httpstatus_list', self.handle_httpstatus_list)
#         if response.status in allowed_statuses:
#             return
#         raise HttpError(response, 'Ignoring non-200 response'