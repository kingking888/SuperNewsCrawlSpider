# # encoding: utf-8
#
# """
#  Created by Andy_Zhong_Spider@163.com on 2019/8/10 下午2:34
#  Function: 新浪新闻爬虫
# """
# import re
# import requests
# import scrapy
# import sys
# from scrapy.linkextractors import LinkExtractor
# from scrapy.spiders import CrawlSpider, Rule
# from scrapy_redis.spiders import RedisCrawlSpider
# from readability import Document
# from hashlib import md5
# from SuperNewsCrawlSpider.items import SupernewscrawlspiderItem
# from SuperNewsCrawlSpider.tools.get_new_time import GetTime
# from SuperNewsCrawlSpider.tools.auto_headers import header_util
#
#
#
# class SupersinaNews(CrawlSpider):
#     name = "sinaNewsSpider"
#     # allowed_domains = ['.*']
#     start_urls = ["https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2509&k=&num=50&page=1"]
#     gt = GetTime()
#     header = header_util()
#
#     custom_settings = {
#         'DOWNLOAD_DELAY': 0.3,
#         # 'DEFAULT_REQUEST_HEADERS': {},
#     }
#
#     def start_requests(self):
#         yield scrapy.Request(url=self.start_urls[0], callback=self.parse_item_home, headers=self.header)
#
#     def parse_item_home(self, response):
#         response = requests.get(response.url)
#         if response.status_code == 200:
#             try:
#                 data = response.json()
#                 datas = data['result']['data']
#                 for dict_data in datas:
#                     if dict_data['url']:
#                         yield scrapy.Request(url=dict_data['url'], callback=self.parse)
#             except:
#                 return
#
#     def parse(self, response):
#         if response.status == 200:
#             html_text = response.text
#             doc = Document(html_text)
#             html = doc.summary()
#             html_size = sys.getsizeof(html_text)
#
#             try:
#                 if response.xpath("""//*[@id="top_bar"]/div/div/span[1]/text()""").extract():
#                     content_time = response.xpath("""//*[@id="top_bar"]/div/div/span[1]/text()""").extract()
#                     public_datetime = str(content_time[0]).replace("年", "-").replace("月", "-").replace("日", "")
#                     public_time = public_datetime + ":00"
#                 else:
#                     if response.xpath("""//*[@id="top_bar"]/div/div[2]/span/text()""").extract():
#                         content_time = response.xpath("""//*[@id="top_bar"]/div/div[2]/span/text()""").extract()
#                         public_datetime = str(content_time[0]).replace("年", "-").replace("月", "-").replace("日", "")
#                         public_time = public_datetime + ":00"
#                     else:
#                         content_time = response.xpath("""//*[@id="pub_date"]/text()""").extract()
#                         public_datetime = str(content_time[0]).replace("年", "-").replace("月", "-").replace("日", " ")
#                         public_time = public_datetime + ":00"
#
#             except:
#                 public_time = ''
#                 # spiderUtil.log_level(8, response.url)
#
#             try:
#                 if response.xpath("""//*[@id="artibody"]/p/text()""").extract():
#                     content_arr = response.xpath("""//*[@id="artibody"]/p/text()""").extract()
#                 else:
#                     content_arr = response.xpath("""//*[@id="article"]/p/text()""").extract()
#                 content = "".join(content_arr)
#             except:
#                 content = ''
#                 # spiderUtil.log_level(7, response.url)
#
#             source = "https://news.sina.com.cn/"
#
#             try:
#                 if response.xpath("""//span[@class="source ent-source"]/text()""").extract():
#                     author = response.xpath("""//span[@class="source ent-source"]/text()""").extract()[0].strip()
#                 else:
#                     try:
#                         pattern = re.compile(r'>责任编辑：(.*?)<',re.DOTALL)
#                         # author = response.xpath("//p[contains(text(),'责任编辑：')]/text()").extract_first()
#                         # author = author.replace("责任编辑：", '')
#                         author = "".join(re.findall(pattern,response.text)).strip().replace(' ','')
#                     except:
#                         author = "新浪网"
#             except:
#                 author = ''
#                 # spiderUtil.log_level(9, response.url)
#
#             try:
#                 if response.xpath("""/html/body/div/h1/text()""").extract():
#                     title = response.xpath("""/html/body/div/h1/text()""").extract()[0]
#                 else:
#                     title = response.xpath("""//*[@id="artibodyTitle"]/text()""").extract()[0]
#             except:
#                 # spiderUtil.log_level(6, response.url)
#                 title = ''
#
#             try:
#                 if content != "":
#                 # if content != "":
#                     item = SupernewscrawlspiderItem()
#                     item["html"] = html
#                     item["source"] = source
#                     item["content"] = content
#                     item["public_time"] = public_time
#                     item["url"] = response.url
#                     item["title"] = title
#                     item["author"] = author
#                     item["crawl_time"] = self.gt.get_time()
#                     item["html_size"] = html_size
#                     item["only_id"] = self.get_md5(item["url"])
#                     # print(item)
#                     yield item
#             except:
#                 pass
#         else:
#             # spiderUtil.log_level(response.status, response.url)
#             return
#
#     def get_md5(self, value):
#         if value:
#             return md5(value.encode()).hexdigest()
#         return ''
#
#
#
#
#
#
#
#
#
#
#
#
#
