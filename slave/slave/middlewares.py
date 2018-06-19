# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from scrapy.http import HtmlResponse
from selenium import webdriver
import os
import random
from scrapy.contrib.downloadermiddleware.useragent import UserAgentMiddleware
from utils.get_proxy import GetIP,GetAllIPs,DeleteIP
from scrapy.selector import Selector

class SlaveSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class SlaveDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class RotateUserAgentMiddleware(UserAgentMiddleware):
    """
        a useragent middleware which rotate the user agent when crawl websites

        if you set the USER_AGENT_LIST in settings,the rotate with it,if not,then use the default user_agent_list attribute instead.
    """

    # the default user_agent_list composes chrome,I E,firefox,Mozilla,opera,netscape
    # for more user agent strings,you can find it in http://www.useragentstring.com/pages/useragentstring.php
    user_agent_list = [
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
        "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
        "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
        "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10"
    ]

    def __init__(self, user_agent=''):
        self.user_agent = user_agent
        super(RotateUserAgentMiddleware).__init__()
        self.user_agent = user_agent

    def _user_agent(self, spider):
        # if hasattr(spider, 'user_agent'):
        #     return spider.user_agent
        # elif self.user_agent:
        #     return self.user_agent

        return random.choice(self.user_agent_list)

    def process_request(self, request, spider):
        ua = self._user_agent(spider)
        if ua:
            request.headers.setdefault('User-Agent', ua)

class RandomProxyMiddleware(object):
    #动态设置ip代理
    # proxies = GetAllIPs()
    def process_request(self, request, spider):

        # if spider.count >= 20:
        #     get_ip = GetIP()
        #     if get_ip != 'no proxy!':
        #         options = webdriver.ChromeOptions()
        #         prefs = {"profile.managed_default_content_settings.images": 2}
        #         options.add_experimental_option("prefs", prefs)
        #         # options.add_argument('user-agent="{0}"'.format(request.headers['User-Agent']))
        #         options.add_argument('--proxy-server={}'.format(get_ip))
        #         options.add_argument(
        #             'user-agent="Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1"')
        #
        #         browser = webdriver.Chrome(
        #             os.path.join(os.path.dirname(os.path.abspath(__file__)),
        #                          'libs/chromedriver'), chrome_options=options)
        #         browser.set_page_load_timeout(3)
        #         browser.set_script_timeout(3)
        #         try:
        #             browser.get('https://h5.m.taobao.com/')
        #         except:
        #             browser.close()
        #             browser.quit()
        #             DeleteIP(get_ip.split('/')[-1])
        #             return
        #         selector = Selector(browser.page_source)
        #         browser.close()
        #         browser.quit()
        #         if selector.css('div[id="main-frame-error"]'):
        #             DeleteIP(get_ip.split('/')[-1])
        #         else:
        #             request.meta["proxy"] = get_ip


        # if self.proxies != []:
        #     proxy = random.choice(self.proxies)
        #     request.meta["proxy"] = proxy
        #     self.proxies.remove(proxy)
        # else:
        #     self.proxies = GetAllIPs()
        get_ip = GetIP()
        if get_ip != 'no proxy!':
            request.meta["proxy"] = get_ip


# Chrome 请求动态网页
# Chrome 请求动态网页
class ChromeMiddleware(object):


    def change_browser(self,request,spider):
        # if spider.count >= 1:
        spider.browser.close()
        spider.browser.quit()
        options = webdriver.ChromeOptions()
        prefs = {"profile.managed_default_content_settings.images": 2}
        options.add_experimental_option("prefs", prefs)
        options.add_argument('user-agent="{0}"'.format(request.headers['User-Agent']))

         # get_ip = GetIP()
         # if get_ip != 'no proxy!':
            # request.meta["proxy"] = get_ip
            # options.add_argument('--proxy-server={}'.format(get_ip))
            #  request.meta["proxy"] = get_ip
        # options.add_argument("--headless")
        # options.add_argument(
        #     'user-agent="Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1"')

        browser = webdriver.Chrome(
            os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         'libs/chromedriver'), chrome_options=options)
        browser.set_window_size(500, 900)
        spider.set_browser(browser)

        # DeleteIP(get_ip.split('/')[-1])

    def process_request(self,request,spider):
        if spider.name == 'taobao':
            try:
                link = 'https://h5.m.taobao.com/awp/core/detail.htm?id='+str(request.url).split('=')[-1]
                # spider.browser.get(link)
                # import time
                # time.sleep(0.5)
                # 处理url的新逻辑，只将https://h5.m.taobao.com/awp/core/detail.htm?id=
                # 的page_source返回，其余均返回为空
                # 在parse中具体判断
                while True:
                    spider.browser.get(link)
                    import time
                    time.sleep(0.5)

                    selector = Selector(HtmlResponse(url=spider.browser.current_url, body=spider.browser.page_source,
                                        encoding="utf-8", request=request))
                    if selector.css('span[data-reactid=".0.0:2.$title_share_default_undefined.0.1"]'):
                        return HtmlResponse(url=spider.browser.current_url, body=spider.browser.page_source,
                                            encoding="utf-8", request=request)
                    elif str(spider.browser.current_url).find('https://h5.m.taobao.com/awp/core/detail.htm?id=') == -1:
                        if str(spider.browser.current_url).find('market') != -1 or str(spider.browser.current_url).find('intl') != -1:
                            self.change_browser(request, spider)
                        return HtmlResponse(url=spider.browser.current_url, body='error', encoding="utf-8",
                                            request=request)
                    else:
                        # if "proxy" in list(request.meta.keys()):
                        #     DeleteIP(request.meta["proxy"].split('/')[-1])
                        self.change_browser(request, spider)

                        # spider.browser.get(link)

                # if str(spider.browser.current_url).find('https://h5.m.taobao.com/awp/core/detail.htm?id=') == -1:
                #     self.change_browser(request, spider)
                #     return HtmlResponse(url=spider.browser.current_url, body='error', encoding="utf-8",request=request)
                # else:

                    # while True:
                    #     selector = Selector(HtmlResponse(url=spider.browser.current_url, body=spider.browser.page_source,
                    #                     encoding="utf-8", request=request))
                        # if selector.css('.main-frame-error'):
                        #     self.change_browser(request,spider)
                        # if selector.css('span[data-reactid=".0.0:2.$title_share_default_undefined.0.1"]'):
                        #     break
                        # else:
                        #     self.change_browser(request, spider)
                        #     spider.browser.get(link)
                    # spider.wait.until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "登录")))

                    # print('visit:', link)
                    # return HtmlResponse(url=spider.browser.current_url, body=spider.browser.page_source,
                    #                     encoding="utf-8", request=request)
                # print(spider.browser.page_source)
                # # 处理淘宝market页面显示的数据
                # if str(spider.browser.current_url).find('market') != -1:
                #     return HtmlResponse(url=request.url, status=500, request=request)
                #     # print('retry'+link)
                #     # while(str(spider.browser.current_url).find('market') != -1):
                #     #     spider.browser.get(link)
                #
                # # 处理飞猪item
                # elif str(spider.browser.current_url).find('trip') != -1:
                #     return HtmlResponse(url=request.url, request=request)
                # # 处理咸鱼拍卖
                # elif str(spider.browser.current_url).find('paimai') != -1:
                #     return HtmlResponse(url=request.url, request=request)
                # # 处理商品不存在
                # elif str(spider.browser.current_url).find('false') == -1:
                #
                # # spider.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#J_recommends > div > div > h2 > span')))
                # import time
                # time.sleep(0.5)
                # print('visit:',link)
                # return HtmlResponse(url=spider.browser.current_url, body=spider.browser.page_source, encoding="utf-8",request=request)
            except Exception as e:

                print(e)
                pass
                # return HtmlResponse(url=spider.browser.current_url, body='error', encoding="utf-8", request=request)