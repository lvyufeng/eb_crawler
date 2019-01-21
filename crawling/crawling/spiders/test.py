# -*- coding: utf-8 -*-
import scrapy


class TestSpider(scrapy.Spider):
    name = 'test'
    allowed_domains = ['test.com']
    start_urls = ['http://test.com/']

    def parse(self, response):
        pass
