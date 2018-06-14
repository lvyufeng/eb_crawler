# -*- coding: utf-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals

class TaobaoSpider(RedisSpider):
    name = 'taobao'
    allowed_domains = ['www.taobao.com']
    # start_urls = ['https://item.taobao.com/item.htm?id=525730909486']

    redis_key = 'taobao:start_urls'



    def __init__(self):
        self.browser = webdriver.Chrome()
        super(TaobaoSpider,self).__init__()
        dispatcher.connect(self.spider_closed,signals.spider_closed)

    def spider_closed(self,spider):
    # 当爬虫退出时，关闭Chrome
        print('spider closed')
        self.browser.quit()

    def parse(self, response):


        pass
