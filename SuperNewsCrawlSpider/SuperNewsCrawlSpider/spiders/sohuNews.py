# encoding: utf-8

"""
 Created by Andy_Zhong_Spider@163.com on 2019/8/10 下午2:34
 Function: 新浪新闻爬虫
"""
import re
import json
import requests
import scrapy
import sys
import time
import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_redis.spiders import RedisCrawlSpider
from readability import Document
from hashlib import md5
from SuperNewsCrawlSpider.items import SupernewscrawlspiderItem
from SuperNewsCrawlSpider.tools.get_new_time import GetTime
from SuperNewsCrawlSpider.tools.auto_headers import header_util



class SupersohuNews(CrawlSpider):
    name = "sohuNewsSpider"
    start_urls = ['http://v2.sohu.com/public-api/feed?scene=CHANNEL&sceneId={}&page=1&size=80']
    gt = GetTime()
    header = header_util()

    custom_settings = {
        'DOWNLOAD_DELAY': 0.3,
        # 'DEFAULT_REQUEST_HEADERS': {},
    }

    def start_requests(self):
        url_list=[15,10,8,17,18,19,23,24,25,26,27,28,29,30,34,38,39,40,41,42,43,44,45,46,47]
        for i in url_list:
            url = self.start_urls[0].format(str(i))
            yield scrapy.Request(url=url, callback=self.parse_item_home, headers=self.header)

    def parse_item_home(self, response):
        url = response.url
        res = requests.get(url,headers=self.header)
        res.encoding = "utf-8"
        if res.status_code == 200:
            try:
                data_str = res.text
                data_str = data_str[1:-1]
                data_str = eval(data_str, type('Dummy', (dict,), dict(__getitem__=lambda s, n: n))())
                data_str = json.dumps(data_str)
                data_str = json.loads(data_str)
                for r in data_str:
                    try:
                        public_time_rt = datetime.datetime.fromtimestamp(r['publicTime'] // 1000)
                        public_time = datetime.datetime.strftime(public_time_rt, '%Y-%m-%d %H:%M:%S')
                    except:
                        # spiderUtil.log_level(8, response.url)
                        public_time = ''
                    try:
                        author = str(r['authorName'])
                    except:
                        # spiderUtil.log_level(9, response.url)
                        author = ''
                    try:
                        title = str(r['title'])
                    except:
                        # spiderUtil.log_level(6, response.url)
                        title = ''
                    url = 'http://www.sohu.com/a/' + str(r['id']) + '_' + str(r['authorId'])

                    yield scrapy.Request(url=url, callback=self.parse, headers=self.header, meta={'public_time':public_time,'url':url,'title':title,'author':author})
            except:
                return

    def parse(self, response):
        if response.status == 200:
            html_text = response.text
            doc = Document(html_text)
            html = doc.summary()
            html_size = sys.getsizeof(html_text)

            try:
                content_arr = response.xpath("""//article//p//text()""").extract()
                content = "".join(content_arr)
            except:
                # spiderUtil.log_level(7, response.url)
                content = ''


            source = "http://news.sohu.com/"

            try:
                if content != "":
                    item = SupernewscrawlspiderItem()
                    item["html"] = html
                    item["public_time"] = response.meta['public_time']
                    item["url"] = response.meta['url']
                    item["title"] = response.meta['title']
                    item["author"] = response.meta['author']
                    item["source"] = source
                    item["content"] = content
                    item["html_size"] = html_size
                    item["crawl_time"] = self.gt.get_time()
                    item["only_id"] = self.get_md5(item["url"])
                    # print(self.item)
                    yield item
            except:
                pass
        else:
            # spiderUtil.log_level(response.status, response.url)
            return

    def get_md5(self, value):
        if value:
            return md5(value.encode()).hexdigest()
        return ''

