# -*- coding: utf-8 -*-

# Scrapy settings for SuperNewsCrawlSpider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'SuperNewsCrawlSpider'

SPIDER_MODULES = ['SuperNewsCrawlSpider.spiders']
NEWSPIDER_MODULE = 'SuperNewsCrawlSpider.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'SuperNewsCrawlSpider (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False
LOG_LEVEL = "DEBUG"

# COMMANDS_MODULE = 'SuperNewsCrawlSpider.commands'

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  'Accept-Language': 'en',
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'SuperNewsCrawlSpider.middlewares.SupernewscrawlspiderSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   # 'SuperNewsCrawlSpider.middlewares.SupernewscrawlspiderDownloaderMiddleware': 543,
    'SuperNewsCrawlSpider.middlewares.RandomUserAgentMidddlware': 543,
    # 'SuperRedisCrawlSpider.middlewares.RandomMyProxyMiddleware': 544,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# EXTENSIONS = {
#     # 'scrapy.extensions.telnet.TelnetConsole': 300,
#     # 'BigB2BSpider.extendions.sendmail.SendEmail': 300,
#     'SuperNewsCrawlSpider.extensions.closespider.CloseSpider': 300,
#     # 'SuperNewsCrawlSpider.extensions.redisspidersmartIdleclosed.RedisSpiderSmartIdleClosedExensions': 301,
#
# }
# MYEXT_ENABLED = True

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'SuperNewsCrawlSpider.pipelines.SupernewscrawlspiderPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

HTTPERROR_ALLOWED_CODES = [404, 302, 403, 301, 500]

MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'ping31415@'
MYSQL_PORT = '3306'
MYSQL_DBNAME = 'spider_data_base'


import os
from datetime import datetime
date = datetime.now()
# 日志文件设置
# LOG_LEVEL = 'DEBUG'
# LOG_LEVEL = 'WARNING'
# LOG_ENCODING = 'utf-8'
# # 判断是否存在log文件夹，不存在则创建
# if os.path.exists('./log'):
#     print('Log folder already exists.Do nothing.')
# else:
#     print('There is no log folder for storage, create!')
#     os.makedirs('log')
# LOG_FILE = 'log/{}-{}-{}T{}_{}_{}.log'.format(date.year, date.month, date.day, date.hour, date.minute, date.second)


# 错误数达到该值时结束爬虫且发送邮件
# CLOSESPIDER_ERRORCOUNT = 1

# # 发送邮件相关设置 QQ邮箱
# # 收件人
# STATSMAILER_RCPTS = ['184108270@qq.com','18942269545@163.com']
# # 项目名
# PROJECT_NAME = '爬虫指定数量错误关闭发送邮件测试'
# # 邮件发送服务器
# MAIL_HOST = 'smtp.qq.com'
# # 发件人地址
# MAIL_FROM = '1500132166@qq.com'
# # 授权码或者密码
# MAIL_PASS = 'ibqhmdvrynaohdja'
# #qiefkahwegvmgcbi
#
# # 邮件发送服务器端口
# MAIL_PORT = 465


# 发送邮件相关设置 163邮箱
# 收件人
STATSMAILER_RCPTS = ['1500132166@qq.com', '184108270@qq.com']
# STATSMAILER_RCPTS = 'liuzc@jianshutech.com,chensy@jianshutech.com,weipan@jianshutech.com'
# 项目名
PROJECT_NAME = '爬虫指定数量错误关闭发送邮件测试'
# 邮件发送服务器
MAIL_HOST = 'smtp.163.com'
# 发件人地址
MAIL_FROM = '18942269545@163.com'
# 授权码或者密码
MAIL_PASS = 'ping1688'
# 邮件发送服务器端口
MAIL_PORT = 25


# RETRY_ENABLED = True                  # 默认开启失败重试，一般关闭
# RETRY_TIMES = 3                         # 失败后重试次数，默认两次
# RETRY_HTTP_CODES = [500, 502, 503, 504, 522, 524, 408]   # 碰到这些验证码，才开启重试

