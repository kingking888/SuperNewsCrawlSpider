# -*- coding: utf-8 -*-
import logging
import requests



# 实现随机代理IP 需运行本地代理池
class RandomMyProxyMiddleware(object):
    logger = logging.getLogger(__name__)
    def process_request(self, request, spider):
        request.meta['proxy'] = 'http://' + self.proxy()

    def proxy(self):
        proxy = requests.get("http://127.0.0.1:5010/get").text
        try:
            print('获取IP代理中---->>>')
            # proxy = requests.get("http://127.0.0.1:5010/get").text
            ip = {"http": "http://" + proxy, "https": "https://" + proxy}
            r = requests.get("http://www.baidu.com", proxies=ip, timeout=4)
            print(r.status_code)
            if r.status_code == 200:
                return proxy
        except:
            print('重新获取IP代理中---->>>')
            self.delete_proxy(proxy)
            return self.proxy()

    def process_response(self, request, response, spider):
        '''对返回的response处理'''
        # 如果返回的response状态不是200，重新生成当前request对象
        if response.status != 200:
            print("again response ip:")
            # 对当前request加上代理
            request.meta['proxy'] = 'http://' + self.proxy()
            return request
        return response

    def process_exception(self, request, exception, spider):
        self.logger.debug('Get exception')
        request.meta['proxy'] = 'http://' + self.proxy()
        return request

    def delete_proxy(self, proxy):
        requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))