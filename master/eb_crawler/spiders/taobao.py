# -*- coding: utf-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
import os

class TaobaoSpider(RedisSpider):
    name = 'taobao'
    allowed_domains = ['www.taobao.com']
    # start_urls = ['https://item.taobao.com/item.htm?id=525730909486']

    redis_key = 'taobao:requests'



    def __init__(self):
        options = webdriver.ChromeOptions()
        prefs = {"profile.managed_default_content_settings.images": 2}
        options.add_experimental_option("prefs", prefs)
        options.add_argument(
            'user-agent="Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1"')

        self.browser = webdriver.Chrome(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'libs/chromedriver'),options=options)
        super(TaobaoSpider,self).__init__()
        dispatcher.connect(self.spider_closed,signals.spider_closed)

    def spider_closed(self,spider):
    # 当爬虫退出时，关闭Chrome
        print('spider closed')
        self.browser.quit()

    def parse(self, response):


        pass
