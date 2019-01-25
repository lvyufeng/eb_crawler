# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import requests
import json
from crawling.items import CrawlingItem

class UrlMasterSpider(scrapy.Spider):
    name = 'url_master'
    count = 0
    # allowed_domains = ['test.com']
    def start_requests(self):
        url_api = {
            # "ali": "https://ai.taobao.com/search/getItem.htm?taobao=true&tmall=true&key={}&maxPageSize=200&page=1",
            # "jd": "https://so.m.jd.com/ware/search._m2wq_list?keyword={}&pagesize=50&page=1",
            # "suning": "https://search.suning.com/emall/mobile/wap/clientSearch.jsonp?keyword={}&ps=20&set=5&ct=-1&cp=0",
            # "ule": "https://m.ule.com/cat/ajax.html?sort=&keyword={}&pageIndex=1",
            "pdd": "http://apiv3.yangkeduo.com/search?q={}&size=50&requery=0&list_id=search_UHpDve&sort=_sales&page=1"
        }

        wb = requests.get('http://202.202.5.140/crawler/three/?lyf')
        keys = json.loads(wb.text)
        for key in keys:
            for platform,api in url_api.items():
                url = api.format(key['three'])

        # for url in self.start_urls:
                yield Request(url=url, callback=self.parse, meta={'key':key['three']}, dont_filter= True)

    # def error_back(self,failure):
    #
    #     # print(failure)
    #     # pass

    def parse(self, response):
        # print(self.task_id)
        content = response.text
        try:
            data = json.loads(content)
            items = data['items']
        except:
            yield Request(response.url, meta={'key': response.meta['key']},
                          callback=self.parse,dont_filter= True)
            return

        equal = response.url.rfind('=') + 1
        page_num = int(response.url.split('=')[-1])
        if page_num == 1:
            for i in range(2,int(data['total']/20)+2):
                yield Request(response.url[0:equal] + str(i), meta={'key':response.meta['key']} ,callback=self.parse,dont_filter= True)

        #
        # for i in range(paginator['pages']):


        for i in items:
            item = CrawlingItem()
            item._values = i
            item._values['key'] = response.meta['key']
            item._values['collection'] = 'temp_pdd'
            yield item
            # yield Request(
            #     'http://apiv4.yangkeduo.com/v5/goods/{}?pdduid='.format(
            #         i['goods_id']),meta={'key':response.meta['key']}, callback=self.parse_detail)

        # yield scrapy.Request('http://www.baidu.com/', callback=self.parse)
    def parse_detail(self,response):
        content = response.text
        try:
            data = json.loads(content)
        except Exception as e:
            yield Request(response.url, meta={'key': response.meta['key']}, callback=self.parse_detail,dont_filter= True)
            return
        data['key'] = response.meta['key']
        item = CrawlingItem()
        item._values = data
        item._values['collection'] = 'temp_pdd_sku'
        yield item
