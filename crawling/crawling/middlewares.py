# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import requests
import random
from queue import Queue
import time
#from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.python import global_object_name
from scrapy.utils.response import response_status_message
import logging

logger = logging.getLogger(__name__)

class CrawlingSpiderMiddleware(object):
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


class CrawlingDownloaderMiddleware(object):
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


class ProxyMiddleWare(object):
    """docstring for ProxyMiddleWare"""
    proxies = Queue()

    def process_request(self, request, spider):
        '''对request对象加上proxy'''
        if self.proxies.qsize() != 0:
            proxy = self.get_random_proxy()
        else:
            self.get_proxies()
            proxy = self.get_random_proxy()
        request.meta['proxy'] = proxy

    def process_response(self, request, response, spider):
        '''对返回的response处理'''
        # 如果返回的response状态不是200，重新生成当前request对象
        if self.proxies.qsize() < 30:
            self.get_proxies()
        if response.status != 200:
            #time.sleep(5)
            reason = response_status_message(response.status)
            return self._retry(request, reason, spider)
        else:
            self.proxies.put(request.meta['proxy'])
        return response

    def process_exception(self,request,exception,spider):
        # spider.logger.info('Get Excepetion, choose another proxy, remain proxy:' + str(self.useful_proxies))
        if self.proxies.qsize() < 30:
            self.get_proxies()

        return self._retry(request, exception, spider)


    def get_proxies(self):
        url = 'http://202.202.5.140:5010/get_all/?name=pdd'
        wb_data = requests.get(url)
        # print(wb_data.content)
        # self.proxies = []
        for i in eval(wb_data.text):
            self.proxies.put('http://' + i)

    def get_random_proxy(self):
        '''随机从文件中读取proxy'''

        proxy = self.proxies.get()
        self.proxies.task_done()
        return proxy

    def _retry(self, request, reason, spider):
        retries = request.meta.get('retry_times', 0) + 1
        stats = spider.crawler.stats
        logger.debug("Retrying %(request)s (failed %(retries)d times): %(reason)s",
                         {'request': request, 'retries': retries, 'reason': reason},
                         extra={'spider': spider})
        retryreq = request.copy()
        retryreq.meta['retry_times'] = retries
        proxy = self.get_random_proxy()
        retryreq.meta['proxy'] = proxy
        retryreq.dont_filter = True
        retryreq.priority = request.priority + 1

        if isinstance(reason, Exception):
            reason = global_object_name(reason.__class__)

        stats.inc_value('retry/count')
        stats.inc_value('retry/reason_count/%s' % reason)
        return retryreq

