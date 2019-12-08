# -*- coding: utf-8 -*-
from fake_useragent import UserAgent



# UserAgentMidddlware
class RandomUserAgentMidddlware(object):
    # 随机更换user-agent
    def __init__(self, crawler):
        super(RandomUserAgentMidddlware, self).__init__()
        # self.ua = UserAgent()
        # 方法一 从配置文件读取随机类型
        # self.ua = UserAgent(use_cache_server=False)
        # 方法二 从json文件读取
        self.path = r"D:\PyhonProject\venv\Projects\SuperNewsCrawlSpider\SuperNewsCrawlSpider\tools\useragent.json"
        self.ua = UserAgent(path=self.path,use_cache_server=False)
        self.ua_type = crawler.settings.get('RANDOM_UA_TYPE', 'random')

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):
        # 通过配置文件的随机类型进行调用
        def get_ua():
            # print(getattr(self.ua, self.ua_type))
            return getattr(self.ua, self.ua_type)
        request.headers.setdefault('User-Agent', get_ua())