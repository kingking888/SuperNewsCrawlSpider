# # encoding: utf-8
#
# """
#  Created by Andy_Zhong_Spider@163.com on 2019/8/10 下午2:34
#  Function: 百度新闻爬虫
# """
# import re
# import random
# import scrapy
# import sys
# import time
# import json
# from scrapy.linkextractors import LinkExtractor
# from scrapy.spiders import CrawlSpider, Rule
# from scrapy_redis.spiders import RedisCrawlSpider
# from readability import Document
# from hashlib import md5
# from lxml import etree
# from SuperNewsCrawlSpider.items import SupernewscrawlspiderItem
# from SuperNewsCrawlSpider.tools.get_new_time import GetTime
# from SuperNewsCrawlSpider.tools.auto_headers import header_util
# from scrapy.cmdline import execute
#
#
# class SuperfenghuangNews(scrapy.Spider):
#     name = "fenghuangNewsSpider"
#     # allowed_domains = ['.*']
#     # http://news.ifeng.com/listpage/11502/20190810/1/rtlist.shtml
#     start_urls = ["http://news.ifeng.com/"]
#     header = header_util()
#     gt = GetTime()
#
#     custom_settings = {
#         'DOWNLOAD_DELAY': 0.3,
#         # 'DEFAULT_REQUEST_HEADERS': {},
#     }
#
#     def start_requests(self):
#         url = self.start_urls[0]
#         yield scrapy.Request(url=url, callback=self.parse, headers=self.header)
#
#     def parse(self,response):
#         news_list = response.xpath("//h2/a/@href").extract()
#         for url in news_list:
#             news_url = "http:" + url
#             yield scrapy.Request(news_url, callback=self.parse_item)
#
#     def parse_item(self,response):
#         if response.status == 200:
#             html_text = response.text
#             doc = Document(html_text)
#             html = doc.summary()
#             html_size = sys.getsizeof(html_text)
#
#             all_arr = response.xpath("""//script//text()""").extract()
#             data = "".join(all_arr).split("allData = ")[1].split("var adData")[0].strip()[:-1]
#             data = json.loads(data)
#             doc = data['docData']
#             try:
#                 public_time = doc['newsTime']
#
#             except:
#                 public_time = ''
#                 # spiderUtil.log_level(8, response.url)
#
#
#             try:
#                 content = doc['contentData']['contentList'][0]['data']
#                 content = "".join(etree.HTML(content).xpath("//p//text()")).strip()
#             except:
#                 content = ''
#                 # spiderUtil.log_level(7, response.url)
#
#             source = "http://news.ifeng.com/"
#
#             try:
#                 author = doc['source']
#             except:
#                 author = ''
#                 # spiderUtil.log_level(9, response.url)
#
#             try:
#                 title = doc['title']
#             except:
#                 title = ''
#                 # spiderUtil.log_level(6, response.url)
#
#             try:
#                 if content != "":
#                     item = SupernewscrawlspiderItem()
#                     item["html"] = html
#                     item["source"] = source
#                     item["content"] = content
#                     item["public_time"] = public_time
#                     item["url"] = response.url
#                     item["title"] = title
#                     item["author"] = author
#                     item["html_size"] = html_size
#                     item["crawl_time"] = self.gt.get_time()
#                     item["only_id"] = self.get_md5(item["url"])
#                     # print(item)
#                     yield item
#             except:
#                 pass
#         else:
#             return
#             # spiderUtil.log_level(response.status, response.url)
#
#     def get_md5(self, value):
#         if value:
#             return md5(value.encode()).hexdigest()
#         return ''