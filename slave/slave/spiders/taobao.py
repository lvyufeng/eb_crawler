# -*- coding: utf-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy.selector import Selector
import os
from items import TaobaoItem,TaobaoItemLoader
from selenium.webdriver.support.ui import WebDriverWait

class TaobaoSpider(RedisSpider):
    name = 'taobao'
    allowed_domains = ['www.taobao.com']

    redis_key = 'taobao:requests'

    def __init__(self):
        self.failed_urls = []
        options = webdriver.ChromeOptions()
        prefs = {"profile.managed_default_content_settings.images": 2}
        options.add_experimental_option("prefs", prefs)
        # options.add_argument(
        #     'user-agent="Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1"')

        self.browser = webdriver.Chrome(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'libs/chromedriver'),chrome_options=options)
        self.browser.set_window_size(500, 900)
        self.browser.set_page_load_timeout(5)
        self.wait = WebDriverWait(self.browser, 5)

        super(TaobaoSpider,self).__init__()
        dispatcher.connect(self.spider_closed,signals.spider_closed)
        dispatcher.connect(self.spider_closed,signals.spider_error)

    def spider_closed(self,spider):
    # 当爬虫退出时，关闭Chrome
        print('spider closed')
        self.browser.quit()
    #     处理失败的url，重新写入redis

    def parse(self, response):
        taobao_item = TaobaoItem()
        """
        1、判断页面是否正确加载，未正确加载，放入failed_urls
        2、解析url内容
        """

        selector = Selector(response)

        # .o-t-error response.status == 404 or
        if selector.css('.o-t-error') or response.status == 500:
            self.failed_urls.append(response.url)
        #     .J_recommends 商品过期不存在 试试其他相似宝贝
        elif str(response.url).split('=')[-1] == 'false':
            print('商品过期不存在,url:{0}'.format(response.url))
        elif str(response.url).find('market') != -1:
            pass
        else:
            item_loader = TaobaoItemLoader(item=TaobaoItem(),response=response)
            item_loader.add_value('productActualID',str(response.url).split('=')[-1])
            item_loader.add_value('productURL',response.url)
            item_loader.add_css('productName','span[data-reactid=".0.0:2.$title_share_default_undefined.0.1"]::text')
            # item_loader.add_xpath('productDescription','')
            # item_loader.add_xpath('shelveDate','')
            item_loader.add_css('weight','dd[data-reactid=".0.1.1.1.0:$基本信息:0:$净含量:0.1"]::text')
            item_loader.add_css('origin','dd[data-reactid=".0.1.1.1.0:$基本信息:0:$产地:0.1"]::text')
            item_loader.add_css('province','dd[data-reactid=".0.1.1.1.0:$基本信息:0:$省份:0.1"]::text')
            item_loader.add_css('city','dd[data-reactid=".0.1.1.1.0:$基本信息:0:$城市:0.1"]::text')
            item_loader.add_css('category','dd[data-reactid=".0.1.1.1.0:$基本信息:0:$种类:0.1"]::text')
            item_loader.add_css('specialtyCategory','dd[data-reactid=".0.1.1.1.0:$基本信息:0:$品类:0.1"]::text')
            item_loader.add_css('brand','dd[data-reactid=".0.1.1.1.0:$基本信息:0:$品牌:0.1"]::text')
            item_loader.add_css('factoryName','dd[data-reactid=".0.1.1.1.0:$基本信息:0:$厂名:0.1"]::text')
            item_loader.add_css('factoryAddress','dd[data-reactid=".0.1.1.1.0:$基本信息:0:$厂地:0.1"]::text')
            item_loader.add_css('series','dd[data-reactid=".0.1.1.1.0:$基本信息:0:$系列:0.1"]::text')
            # item_loader.add_css('specification','dd[data-reactid=".0.1.1.1.0:$基本信息:0:$净含量:0.1"]::text')
            item_loader.add_css('deliveryStartArea','p[data-reactid=".0.0:2.$subinfo_normalTariff_undefined.$subinfo_2"]::text')
            item_loader.add_css('productPrice','del[data-reactid=".0.0:2.$price_default_undefined.0.1.$price_ex_0.2"]')
            item_loader.add_css('productPromPrice','span[data-reactid=".0.0:2.$price_default_undefined.0.0.1.0"]')
            item_loader.add_css('monthSaleCount','p[data-reactid=".0.0:2.$subinfo_normalTariff_undefined.$subinfo_1"]::text')
            item_loader.add_css('commentCount','h3[data-reactid=".0.0:2.$rate_header_default_undefined.0"]::text')

            item_loader.add_css('storeName','h3[data-reactid=".0.0:2.$shop_header_default_undefined.1.0.0"]::text')
            # data-reactid=".0.1.1.1.0:$基本信息:0:$净含量:0.1"
            # item_loader.add_xpath('productActualID','')
            # item_loader.add_xpath('productActualID','')

            taobao_item = item_loader.load_item()

        yield taobao_item

        # pass
