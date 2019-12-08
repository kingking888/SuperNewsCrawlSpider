from scrapy import cmdline

# 在scrapy项目中添加start.py文件，用于启动爬虫
from scrapy import cmdline
# 在爬虫运行过程中，会自动将状态信息存储在crawls/storeMyRequest目录下，支持续爬
# cmdline.execute('scrapy crawl awp914 -s JOBDIR=crawls/storeMyRequest'.split())
# Note:若想支持续爬，在ctrl+c终止爬虫时，只能按一次，爬虫在终止时需要进行善后工作，切勿连续多次按ctrl+c

cmdline.execute('scrapy crawl baiduNewsSpider'.split())
# cmdline.execute('scrapy crawl sinaNewsSpider'.split())
# cmdline.execute("scrapy crawl sohuNewsSpider".split())
# cmdline.execute("scrapy crawl xinhuaNewsSpider".split())
# cmdline.execute("scrapy crawl fenghuangNewsSpider".split())
# cmdline.execute("scrapy crawl news_test_demo".split())

# # print("scrapy crawl sohuNewsSpider".split())