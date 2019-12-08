# 项目名称
BOT_NAME = 'downloadmiddler'

# 爬虫存储的文件路径
SPIDER_MODULES = ['downloadmiddler.spiders']

# 创建爬虫文件的模板,创建好的文件存放在这个目录下
NEWSPIDER_MODULE = 'downloadmiddler.spiders'

# 模拟浏览器请求
USER_AGENT = 'downloadmiddler (+http://www.yourdomain.com)'

# 设置是否遵守robots协议,默认TRUE遵守
ROBOTSTXT_OBEY = False

# 设置请求最大的并发数量(下载器处理的最大数量),默认16个
CONCURRENT_REQUESTS = 32

# 设置请求下载延时,默认为0.
DOWNLOAD_DELAY = 3

# 设置网站的最大并发请求数量,默认8个
CONCURRENT_REQUESTS_PER_DOMAIN = 16

# 设置某个IP下的最大并发请求数量,默认0个,如果非0,要注意网站并发就无效,请求的并发数量将只针对于IP,如果非零,下载延时则针对IP,而不是网站
CONCURRENT_REQUESTS_PER_IP = 16

# 是否携带cookie,默认为TRUE
COOKIES_ENABLED = False

# 是一个终端的扩展插件
TELNETCONSOLE_ENABLED = False

# 设置默认的请求头(cookie不要放在这里)
DEFAULT_REQUEST_HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }

# 设置和激活爬虫中间键
SPIDER_MIDDLEWARES = {
       'downloadmiddler.middlewares.DownloadmiddlerSpiderMiddleware': 543,
    }

# 设置和激活下载中间键
DOWNLOADER_MIDDLEWARES = {
        'downloadmiddler.middlewares.SeleniumDownloadMiddlerware': 543
    }

# 设置和激活管道文件,数字表示优先级,越小越高
ITEM_PIPELINES = {
       'downloadmiddler.pipelines.DownloadmiddlerPipeline': 300,
    }

# 设置扩展
EXTENSIONS = {
       'scrapy.extensions.telnet.TelnetConsole': None,
    }

# 自动限速的扩展,上一个请求和下一个请求之间的时间是不固定的,默认情况下,自动限速扩是没有打开的False
AUTOTHROTTLE_ENABLED = True

# 初始的下载延时,默认为5秒
AUTOTHROTTLE_START_DELAY = 5

# 最大下载延时
AUTOTHROTTLE_MAX_DELAY = 60

# 针对于网站的最大的并行请求数量
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0

# debug调试模式,默认为False
AUTOTHROTTLE_DEBUG = False

# 设置数据缓存,默认不开启
HTTPCACHE_ENABLED = True

# 设置缓存的超时时间,为0代表永久有效
HTTPCACHE_EXPIRATION_SECS = 0

# 设置缓存数据的存储路径
HTTPCACHE_DIR = 'httpcache'

# 忽略某些状态码的请求结果
HTTPCACHE_IGNORE_HTTP_CODES = []

# 开启缓存的一个扩展插件
HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# cookie debug模式,默认为Fales
COOKIES_DEBUG = True

# 关于日志信息设置

# Scrapy提供5层logging级别:

# CRITICAL - 严重错误(critical)
# ERROR    - 一般错误(regular errors)
# WARNING  - 警告信息(warning messages)
# INFO     - 一般信息(informational messages)
# DEBUG    - 调试信息(debugging messages)
