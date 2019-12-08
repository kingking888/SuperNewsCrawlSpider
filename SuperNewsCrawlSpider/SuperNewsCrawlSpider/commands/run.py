# from scrapy.utils.project import get_project_settings
# from SuperRedisCrawlSpider.utils import get_config
# from scrapy.crawler import CrawlerProcess
#
#
# def run():
#     # 获取命令行参数
#     name = "china"
#     # name = sys.argv[1]
#     custom_settings = get_config(name)
#     # 获取爬虫名字
#     # print(custom_settings)
#     spider = custom_settings.get('spider','Powerfull')
#     # 获取项目默认配置
#     project_settings = get_project_settings()
#     settings = dict(project_settings.copy())
#     # 合并配置
#     settings.update(custom_settings.get('settings'))
#     process = CrawlerProcess(settings)
#     # 启动爬虫
#     process.crawl(spider, **{'name': name})
#     process.start()
#
# if __name__ == '__main__':
#     run()