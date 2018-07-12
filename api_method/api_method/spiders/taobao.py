# -*- coding: utf-8 -*-
import scrapy
from utils.get_urls import get_urls
from utils.get_proxy import GetAllIPs
import json
import random

class TaobaoSpider(scrapy.Spider):
    name = 'taobao'
    allowed_domains = ['taobao.com']
    urls = get_urls('/Users/lvyufeng/PycharmProjects/eb_crawler/api_method/api_method/utils/taskinfo.csv')
    proxies = GetAllIPs()

    def start_requests(self):

        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse, meta={'proxy': 'http://'+random.choice(self.proxies)})

    def parse(self, response):
        # print(len(self.start_urls))
        if response:
            data = json.loads(response.text)
            if data['ret'][0] == 'FAIL_SYS_USER_VALIDATE::哎哟喂,被挤爆啦,请稍后重试!':
                print('FAIL_SYS_USER_VALIDATE::哎哟喂,被挤爆啦,请稍后重试!')
            else:
                print(data)
        else:
            print(response.url)
        pass

