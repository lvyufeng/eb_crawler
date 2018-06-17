# -*- coding: utf-8 -*-
from scrapy_redis.spiders import RedisSpider
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
import os
from items import TaobaoItem,TaobaoItemLoader
from selenium.webdriver.support.ui import WebDriverWait
from utils.redis_op import insert_data,redis_connect

class TaobaoSpider(RedisSpider):
    name = 'taobao'
    # allowed_domains = ['www.taobao.com']

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
        # self.browser.
        self.browser.set_page_load_timeout(5)
        self.wait = WebDriverWait(self.browser, 5)

        super(TaobaoSpider,self).__init__()
        dispatcher.connect(self.spider_closed,signals.spider_closed)
        dispatcher.connect(self.write_back_failed_urls,signals.spider_error)
        dispatcher.connect(self.write_back_failed_urls, signals.item_dropped)


    def write_back_failed_urls(self):
        host = self.crawler.settings.get('REDIS_HOST')
        port = self.crawler.settings.get('REDIS_PORT')
        db = 0
        r = redis_connect(host, port, db)
        if r != None:
            for url in self.failed_urls:
                try:
                    print(type,url)
                    insert_data(r, 'taobao:requests', url)
                except Exception as e:
                    print(url)
                    print(e)
                    break
            print('failed urls write back finished')
        else:
            print('can not connect redis')

    # 处理失败的url，重新写入redis
    def spider_closed(self):
    # 当爬虫退出时，关闭Chrome
        print('spider closed')
        self.browser.quit()


    def parse(self, response):
        taobao_item = TaobaoItem()
        """
        1、判断页面是否正确加载，未正确加载，放入failed_urls
        2、解析url内容
        """

        # selector = Selector(response)
        #
        # # .o-t-error response.status == 404 or
        # if selector.css('.o-t-error') or response.status == 500 or str(response.url).find('market') != -1:
        #     self.failed_urls.append(response.url)
        #     print('加载错误，重新写回redis')
        # #     .J_recommends 商品过期不存在 试试其他相似宝贝
        # # elif selector.css('.hintBanner')
        # elif str(response.url).split('=')[-1] == 'false':
        #     print('商品过期不存在,url:{0}'.format(response.url))
        # elif str(response.url).find('trip') != -1:
        #     print('飞猪链接,url:{0}'.format(response.url))
        # else:
        if str(response.url).find('https://h5.m.taobao.com/awp/core/detail.htm?id=') != -1 and response.body != '':
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
        # 处理商品不存在
        elif str(response.url).split('=')[-1] == 'false':
            print('商品过期不存在,url:{0}'.format(response.url))
        # 处理飞猪item
        elif str(response.url).find('trip') != -1:
            print('飞猪链接,url:{0}'.format(response.url))
        # 处理咸鱼拍卖
        elif str(response.url).find('paimai') != -1:
            print('闲鱼链接,url:{0}'.format(response.url))
        else:
            self.failed_urls.append(response.url)
            print('加载错误，重新写回redis')

        yield taobao_item

        # pass
