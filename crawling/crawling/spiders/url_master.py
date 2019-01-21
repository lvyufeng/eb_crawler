# -*- coding: utf-8 -*-
from scrapy_redis.spiders import RedisSpider
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
import os
from scrapy.http import Request
from scrapy.utils.reqser import request_to_dict
import pickle

class UrlSpider(RedisSpider):
    name = 'url_master'
    # allowed_domains = ['www.taobao.com']

    redis_key = 'sku:ali'

    def __init__(self):

        super(UrlSpider,self).__init__()


    def make_requests_from_url(self, url):
        # print(url)
        return Request('https://www.baidu.com', dont_filter=True)

    def parse(self, response):
        print(response)
        pass

        # pass