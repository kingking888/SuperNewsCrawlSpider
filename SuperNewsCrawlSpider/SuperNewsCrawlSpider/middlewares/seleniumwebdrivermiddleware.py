# from scrapy.http import HtmlResponse
# from selenium import webdriver
# from selenium.common.exceptions import TimeoutException
# from SuperNewsCrawlSpider.tools.driverconfig import *



# class ChromeDownloaderMiddleware(object):
#
#     def __init__(self):
#         options = webdriver.ChromeOptions()
#         options.add_argument('--headless')  # 设置无界面
#         if CHROME_PATH:
#             options.binary_location = CHROME_PATH
#         if CHROME_DRIVER_PATH:
#             self.driver = webdriver.Chrome(chrome_options=options, executable_path=CHROME_DRIVER_PATH)  # 初始化Chrome驱动
#         else:
#             self.driver = webdriver.Chrome(chrome_options=options)  # 初始化Chrome驱动
#
#     def __del__(self):
#         self.driver.close()
#
#     def process_request(self, request, spider):
#         try:
#             print('Chrome driver begin...')
#             self.driver.get(request.url)  # 获取网页链接内容
#             return HtmlResponse(url=request.url, body=self.driver.page_source, request=request, encoding='utf-8',
#                                 status=200)  # 返回HTML数据
#         except TimeoutException:
#             return HtmlResponse(url=request.url, request=request, encoding='utf-8', status=500)
#         finally:
#             print('Chrome driver end...')



# -*- coding: utf-8 -*-

# from selenium import webdriver
# from selenium.common.exceptions import TimeoutException
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from scrapy.http import HtmlResponse
# from logging import getLogger


# class SeleniumMiddleware():
#     def __init__(self, timeout=None, service_args=[]):
#         self.logger = getLogger(__name__)
#         self.timeout = timeout
#         self.browser = webdriver.PhantomJS(service_args=service_args)
#         self.browser.set_window_size(1400, 700)
#         self.browser.set_page_load_timeout(self.timeout)
#         self.wait = WebDriverWait(self.browser, self.timeout)
#
#     def __del__(self):
#         self.browser.close()
#
#     def process_request(self, request, spider):
#         """
#         用PhantomJS抓取页面
#         :param request: Request对象
#         :param spider: Spider对象
#         :return: HtmlResponse
#         """
#         self.logger.debug('PhantomJS is Starting')
#         page = request.meta.get('page', 1)
#         try:
#             self.browser.get(request.url)
#             if page > 1:
#                 input = self.wait.until(
#                     EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager div.form > input')))
#                 submit = self.wait.until(
#                     EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager div.form > span.btn.J_Submit')))
#                 input.clear()
#                 input.send_keys(page)
#                 submit.click()
#             self.wait.until(
#                 EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#mainsrp-pager li.item.active > span'), str(page)))
#             self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.m-itemlist .items .item')))
#             return HtmlResponse(url=request.url, body=self.browser.page_source, request=request, encoding='utf-8',
#                                 status=200)
#         except TimeoutException:
#             return HtmlResponse(url=request.url, status=500, request=request)
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         return cls(timeout=crawler.settings.get('SELENIUM_TIMEOUT'),
#                    service_args=crawler.settings.get('PHANTOMJS_SERVICE_ARGS'))


"""This module contains the ``SeleniumMiddleware`` scrapy middleware"""

from importlib import import_module

from scrapy import signals
from scrapy.exceptions import NotConfigured
from scrapy.http import HtmlResponse
from selenium.webdriver.support.ui import WebDriverWait
from .http import SeleniumRequest



class SeleniumMiddleware:
    """Scrapy middleware handling the requests using selenium"""

    def __init__(self, driver_name, driver_executable_path, driver_arguments,
        browser_executable_path):
        """Initialize the selenium webdriver
        Parameters
        ----------
        driver_name: str
            The selenium ``WebDriver`` to use
        driver_executable_path: str
            The path of the executable binary of the driver
        driver_arguments: list
            A list of arguments to initialize the driver
        browser_executable_path: str
            The path of the executable binary of the browser
        """

        webdriver_base_path = f'selenium.webdriver.{driver_name}'

        driver_klass_module = import_module(f'{webdriver_base_path}.webdriver')
        driver_klass = getattr(driver_klass_module, 'WebDriver')

        driver_options_module = import_module(f'{webdriver_base_path}.options')
        driver_options_klass = getattr(driver_options_module, 'Options')

        driver_options = driver_options_klass()
        if browser_executable_path:
            driver_options.binary_location = browser_executable_path
        for argument in driver_arguments:
            driver_options.add_argument(argument)

        driver_kwargs = {
            'executable_path': driver_executable_path,
            f'{driver_name}_options': driver_options
        }

        self.driver = driver_klass(**driver_kwargs)

    @classmethod
    def from_crawler(cls, crawler):
        """Initialize the middleware with the crawler settings"""

        driver_name = crawler.settings.get('SELENIUM_DRIVER_NAME')
        driver_executable_path = crawler.settings.get('SELENIUM_DRIVER_EXECUTABLE_PATH')
        browser_executable_path = crawler.settings.get('SELENIUM_BROWSER_EXECUTABLE_PATH')
        driver_arguments = crawler.settings.get('SELENIUM_DRIVER_ARGUMENTS')

        if not driver_name or not driver_executable_path:
            raise NotConfigured(
                'SELENIUM_DRIVER_NAME and SELENIUM_DRIVER_EXECUTABLE_PATH must be set'
            )

        middleware = cls(
            driver_name=driver_name,
            driver_executable_path=driver_executable_path,
            driver_arguments=driver_arguments,
            browser_executable_path=browser_executable_path
        )

        crawler.signals.connect(middleware.spider_closed, signals.spider_closed)

        return middleware

    def process_request(self, request, spider):
        """Process a request using the selenium driver if applicable"""

        if not isinstance(request, SeleniumRequest):
            return None

        self.driver.get(request.url)

        for cookie_name, cookie_value in request.cookies.items():
            self.driver.add_cookie(
                {
                    'name': cookie_name,
                    'value': cookie_value
                }
            )

        if request.wait_until:
            WebDriverWait(self.driver, request.wait_time).until(
                request.wait_until
            )

        if request.screenshot:
            request.meta['screenshot'] = self.driver.get_screenshot_as_png()

        if request.script:
            self.driver.execute_script(request.script)

        body = str.encode(self.driver.page_source)

        # Expose the driver via the "meta" attribute
        request.meta.update({'driver': self.driver})

        return HtmlResponse(
            self.driver.current_url,
            body=body,
            encoding='utf-8',
            request=request
        )

    def spider_closed(self):
        """Shutdown the driver when spider is closed"""
        self.driver.quit()