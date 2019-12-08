# -*- coding: utf-8 -*-

import logging
import requests
import json



class WeiBoMiddleWare(object):
    def __init__(self, cookies_pool_url):
        self.logging = logging.getLogger("WeiBoMiddleWare")
        self.cookies_pool_url = cookies_pool_url

    def get_random_cookies(self):
        try:
            response = requests.get(self.cookies_pool_url)
        except Exception as e:
            self.logging.info('Get Cookies failed: {}'.format(e))
        else:
            # 在中间件中，设置请求头携带的Cookies值，必须是一个字典，不能直接设置字符串。
            cookies = json.loads(response.text)
            self.logging.info('Get Cookies success: {}'.format(response.text))
            return cookies

    @classmethod
    def from_settings(cls, settings):
        obj = cls(
            cookies_pool_url=settings['WEIBO_COOKIES_URL']
        )
        return obj

    def process_request(self, request, spider):
        request.cookies = self.get_random_cookies()
        return None
