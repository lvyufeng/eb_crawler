# -*- coding: utf-8 -*-
import scrapy
import pymongo
from scrapy.http import Request
import json
from crawling.items import CrawlingItem

class PddSkuSpider(scrapy.Spider):
    name = 'pdd_sku'
    allowed_domains = ['yangkeduo.com']
    start_urls = ['http://yangkeduo.com/']
    client = pymongo.MongoClient('202.202.5.140')
    db = client['test']
    collecetion = db['temp_pdd']

    def start_requests(self):

        for i in self.collecetion.find():
            yield Request('http://apiv4.yangkeduo.com/v5/goods/{}?pdduid='.format(i['goods_id']), callback=self.parse, meta={'key':i['key']})


    def parse(self, response):
        content = response.text
        try:
            data = json.loads(content)
        except:
            yield Request(response.url, meta={'key':response.meta['key']},
                          callback=self.parse)
            return
        item = CrawlingItem()
        item._values = data
        item._values['key'] = response.meta['key']
        yield item

