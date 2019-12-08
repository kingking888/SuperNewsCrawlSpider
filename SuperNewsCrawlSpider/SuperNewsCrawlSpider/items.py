# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy



class SupernewscrawlspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    html = scrapy.Field()
    only_id = scrapy.Field()
    source = scrapy.Field()
    content = scrapy.Field()
    public_time = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    crawl_time = scrapy.Field()
    html_size = scrapy.Field()
