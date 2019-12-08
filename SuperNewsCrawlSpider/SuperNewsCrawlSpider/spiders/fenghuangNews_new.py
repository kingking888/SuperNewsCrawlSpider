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
# import datetime
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
# from extractors.AutoExtractors import *
#
#
# class SuperfenghuangNews(scrapy.Spider):
#     name = "fenghuangNewsSpider"
#     today_time = datetime.datetime.now().strftime('%Y%m%d')
#     # print(today_time)
#     # allowed_domains = ['.*']
#     start_urls = ["http://news.ifeng.com/listpage/11502/{}/1/rtlist.shtml"]
#     header = header_util()
#     gt = GetTime()
#
#     custom_settings = {
#         'DOWNLOAD_DELAY': 0.3,
#         # 'DEFAULT_REQUEST_HEADERS': {},
#     }
#
#     def start_requests(self):
#         url = self.start_urls[0].format(self.today_time)
#         yield scrapy.Request(
#             url=url,
#             callback=self.parse_item,
#             headers=self.header
#         )
#
#     def parse_item(self,response):
#         if response.status == 200:
#             li_list = response.xpath("//div[@class='main']//div[@class='newsList']//ul//li")
#             for li in li_list:
#                 item = SupernewscrawlspiderItem()
#                 the_time = li.xpath(".//h4/text()").extract_first()
#                 news_href = li.xpath(".//a/@href").extract_first()
#                 item["title"] = li.xpath(".//a/text()").extract_first()
#                 # item["public_time"] = datetime.datetime.now().strftime('%Y') \
#                 #                       + "-" + the_time.split(' ')[0].replace('/','-') \
#                 #                       + " " + the_time.split(' ')[-1] + ":00"
#                 if news_href:
#                     yield scrapy.Request(
#                         url=news_href,
#                         callback=self.parse_news_detail,
#                         meta={"item": item},
#                         dont_filter=True
#                     )
#             next_page_url = response.xpath("//div[@class='nextPage']//a[contains(text(),'下一页 ')]"
#                                            "/@href").extract_first()
#             if next_page_url:
#                 yield scrapy.Request(
#                     url=next_page_url,
#                     callback=self.parse_item
#                 )
#
#     def parse_news_detail(self, response):
#         item = response.meta["item"]
#         html_text = response.text
#         result = SuperAutoExtract().get_all(html_text)
#         print(result)
#
#         # doc = Document(html_text)
#         # html = doc.summary()
#         # html_size = sys.getsizeof(html_text)
#         #
#         # item["html"] = ''
#         # item["html_size"] = html_size
#         # if html_text:
#         #     try:
#         #         all_arr = response.xpath("""//script//text()""").extract()
#         #         data = "".join(all_arr).split("allData = ")[1].split("var adData")[0].strip()[:-1]
#         #         data = json.loads(data)
#         #         doc = data['docData']
#         #         try:
#         #             item["public_time"] = doc['newsTime']
#         #         except:
#         #             item["public_time"] = ''
#         #             # spiderUtil.log_level(8, response.url)
#         #
#         #
#         #         try:
#         #             item["content"] = doc['contentData']['contentList'][0]['data']
#         #             item["content"] = "".join(etree.HTML(item["content"]).xpath("//p//text()")).strip()
#         #         except:
#         #             item["content"] = ''
#         #             # spiderUtil.log_level(7, response.url)
#         #
#         #         item["source"] = "http://news.ifeng.com/"
#         #
#         #         try:
#         #             # weMediaName
#         #             item["author"] = doc['source']
#         #         except:
#         #             item["author"] = ''
#         #             # spiderUtil.log_level(9, response.url)
#         #
#         #         try:
#         #             item["title"] = doc['title']
#         #         except:
#         #             item["title"] = item["title"]
#         #         item["url"] = response.url
#         #         item["crawl_time"] = self.gt.get_time()
#         #         item["only_id"] = self.get_md5(item["url"])
#         #         yield item
#         #     except:
#         #         return
#
#
#         #                 # spiderUtil.log_level(6, response.url)
#         # item["content"] = "".join(response.xpath("//div[@id='root']//div[@class='text-3zQ3cZD4']//text()").extract())
#         # item["author"] = "".join(response.xpath("//span[contains(text(),'来源：')]/following-sibling::span//a/text()").extract_first())
#         # item["public_time"] = response.xpath("//p[contains(@class,'time-hm3v7ddj')]/span[1]/text()").extract_first()
#
#         # if item["public_time"]:
#         #     item["public_time"] = item["public_time"].replace("年","-").replace("月","-").replace("日","")
#         # else:
#         #     item["public_time"] = ''
#         # source = "http://news.ifeng.com/"
#         # item["source"] = source
#
#
#
#
#     def get_md5(self, value):
#         if value:
#             return md5(value.encode()).hexdigest()
#         return ''