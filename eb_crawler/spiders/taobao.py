# -*- coding: utf-8 -*-
import scrapy


class TaobaoSpider(scrapy.Spider):
    name = 'taobao'
    allowed_domains = ['www.taobao.com']
    start_urls = ['https://item.taobao.com/item.htm?id=525730909486']

    def parse(self, response):
        pass
