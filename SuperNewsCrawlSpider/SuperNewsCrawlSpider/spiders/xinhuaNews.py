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
# from SuperNewsCrawlSpider.tools.readability import Readability
from extractors.AutoExtractors import *



class SupersohuNews(scrapy.Spider):
    name = "xinhuaNewsSpider"
    start_urls = ["http://qc.wa.news.cn/nodeart/list?nid=11147664&pgnum={}&cnt={}&tp=1&orderby=1"]
    header = header_util()
    gt = GetTime()

    custom_settings = {
        'DOWNLOAD_DELAY': 0.3,
        # 'DEFAULT_REQUEST_HEADERS': {},
    }

    def start_requests(self):
        num = 30000
        pgnum = 1
        while num / 200 > 0:
            cnt = (num - 1) % 200 + 1
            url = str(self.start_urls[0]).format(pgnum, cnt)
            pgnum += 1
            num -= cnt
            yield scrapy.Request(url=url, callback=self.parse_item_home, headers=self.header)

    def parse_item_home(self, response):
        if response.text != None:
            data_str = response.text
            data_str = data_str[1:-1]
            data_str = eval(data_str, type('Dummy', (dict,), dict(__getitem__=lambda s, n: n))())
            data_str = json.dumps(data_str)
            data_str = json.loads(data_str)
            if data_str:
                try:
                    data_str = data_str['data']['list']
                except:
                    return
                if data_str:
                    for r in data_str:
                        try:
                            # r['PubTime']
                            public_time = str(r['PubTime'])
                        except:
                            # spiderUtil.log_level(8, response.url)
                            public_time = ''
                        try:
                            author = str(r['Author']).strip()
                        except:
                            # spiderUtil.log_level(9, response.url)
                            author = ''
                        try:
                            title = str(r['Title'])
                        except:
                            # spiderUtil.log_level(6, response.url)
                            title = ''
                        r_url = r['LinkUrl']
                        public_time = public_time
                        title = title
                        author = author
                        yield scrapy.Request(
                            url=r_url,
                            callback=self.parse_item,
                            headers=self.header,
                            meta={
                                "public_time":public_time,
                                "title":title,
                                "author":author,
                            }
                        )


    def parse_item(self, response):
        if response.status == 200:
            html_text = response.text
            result = SuperAutoExtract().get_all(html_text)
            print(result)

        #     doc = Document(html_text)
        #     html = doc.summary()
        #     # print(doc.get_clean_html())
        #     html_size = sys.getsizeof(html_text)
        #
        #     try:
        #         content_arr = response.xpath("""//div[contains(@id,'detail')]//p/text()""").extract()
        #         content = "".join(content_arr).replace('\u3000','').replace('\xa0','')
        #     except:
        #         # spiderUtil.log_level(7, response.url)
        #         content = ''
        #
        #     author = response.meta['author']
        #     if author != "null":
        #         author = author
        #     else:
        #         pattern = re.compile(r'\（记者.*?\）|\(.*?\)', re.DOTALL)
        #         author = "".join(re.findall(pattern, content)).strip()
        #         if "记者" and "（" in author:
        #             try:
        #                 author = author.split(' ')[-1].replace('）','')
        #             except:
        #                 author = ''
        #         elif '(' in author:
        #             pattern = re.compile(r'(.*?)',re.DOTALL)
        #             author = "".join(re.findall(pattern,author)[-1])
        #         else:
        #             author = author
        #
        #
        #     source = "http://www.xinhuanet.com/"
        #
        #     try:
        #         if content != "":
        #             item = SupernewscrawlspiderItem()
        #             item["html"] = html
        #             item["source"] = source
        #             item["content"] = content
        #             item["public_time"] = response.meta["public_time"]
        #             item["url"] = response.url
        #             item["title"] = response.meta["title"]
        #             item["author"] = author
        #             item["html_size"] = html_size
        #             item["crawl_time"] = self.gt.get_time()
        #             item["only_id"] = self.get_md5(item["url"])
        #             # print(item)
        #             yield item
        #     except:
        #         pass
        # else:
        #     return
            # spiderUtil.log_level(response.status, response.url)

    def get_md5(self, value):
        if value:
            return md5(value.encode()).hexdigest()
        return ''



