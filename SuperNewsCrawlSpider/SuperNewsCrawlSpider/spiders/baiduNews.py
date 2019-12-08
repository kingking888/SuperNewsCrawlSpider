# encoding: utf-8

"""
 Created by Andy_Zhong_Spider@163.com on 2019/8/10 下午2:34
 Function: 百度新闻爬虫
"""
import re
import random
import scrapy
import sys
import time
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_redis.spiders import RedisCrawlSpider
from readability import Document
from hashlib import md5
from SuperNewsCrawlSpider.items import SupernewscrawlspiderItem
from SuperNewsCrawlSpider.tools.get_new_time import GetTime
from SuperNewsCrawlSpider.tools.auto_headers import header_util
from scrapy.cmdline import execute
from extractors.AutoExtractors import *



class SuperbaiduSpider(CrawlSpider):
    name = "baiduNewsSpider"
    allowed_domains = ['.*']
    start_urls = ['https://news.baidu.com/']
    # header = header_util()
    gt = GetTime()

    custom_settings = {
        'DOWNLOAD_DELAY': 0.3,
        # 'DEFAULT_REQUEST_HEADERS': {},
    }


    def start_requests(self):
        url = self.start_urls[0]
        yield scrapy.Request(
            url=url,
            callback=self.parse,
            dont_filter=True
        )

    def parse(self, response):
        li_list = response.xpath("//div[@id='menu']//div[@class='menu-list']//ul//li")[1:13]
        for li in li_list:
            kind_name = li.xpath("./a/text()").extract_first()
            kind_href = li.xpath("./a/@href").extract_first()
            if kind_href:
                kind_href = "https://news.baidu.com" + kind_href
                yield scrapy.Request(
                    url=kind_href,
                    callback=self.parse_news_list,
                    dont_filter=True
                )

    def parse_news_list(self, response):
        a_list = response.xpath("//div[@id='body']//div[contains(@class,'column')]//ul//li//a")
        for a in a_list:
            news_title = a.xpath("./text()").extract_first()
            news_href = a.xpath("./@href").extract_first()
            if news_href:
                yield scrapy.Request(
                    url=news_href,
                    callback=self.parse_item,
                    dont_filter=True
                )

    def parse_item(self, response):
        item = SupernewscrawlspiderItem()
        if response.status == 200:
            # pattern = re.compile(r'<div class="article-title"><h2>(.*?)</h2></div>',re.DOTALL)
            # pattern1 = re.compile(r'<p class="author-name">(.*?)</p>',re.DOTALL)
            # pattern2 = re.compile(r'<span class="date">发布时间：(.*?)</span><span class="time">(.*?)</span>',re.DOTALL)
            # pattern3 = re.compile(r'<span class="account-authentication">(.*?)</span>',re.DOTALL)
            html_text = response.body.decode("utf-8")
            result = SuperAutoExtract().get_all(html_text)
            print(result)
        #     doc = Document(html_text)
        #     html = doc.summary()
        #     html_size = sys.getsizeof(html_text)
        #     try:
        #         content_time = re.search(pattern2,response.text)
        #         public_time = str(time.strftime('%Y', time.localtime(time.time()))) + "-" + str(content_time[1]) \
        #                       + " " + str(content_time[2]) + ":00"
        #     except:
        #         # spiderUtil.log_level(8, response.url)
        #         public_time = ''
        #         pass
        #     try:
        #         content_arr = response.xpath("""//*[@id="article"]/div/p/span/text()""").extract()
        #         content = "".join(content_arr)
        #     except:
        #         content = ''
        #
        #     source = "http://news.baidu.com/"
        #
        #     try:
        #         author_arr = re.findall(pattern1,response.text)
        #         author = "".join(author_arr)
        #     except:
        #         author = ''
        #
        #     try:
        #         title_arr = re.findall(pattern,response.text)
        #         title = "".join(title_arr)
        #     except:
        #         title = ''
        #
        #     try:
        #         if content != "":
        #             item["html"] = html
        #             item["source"] = source
        #             item["content"] = content
        #             item["public_time"] = public_time
        #             item["url"] = response.url
        #             item["title"] = title
        #             item["author"] = author
        #             item["crawl_time"] = self.gt.get_time()
        #             item["html_size"] = html_size
        #             item["only_id"] = self.get_md5(item["url"])
        #             # print(item)
        #             yield item
        #     except:
        #         pass
        # else:
        #     return

    def get_md5(self, value):
        if value:
            return md5(value.encode()).hexdigest()
        return ''



if __name__ == '__main__':
    execute(["scrapy", "crawl", "baiduNewsSpider"])