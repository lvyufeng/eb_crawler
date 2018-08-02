import spider
import requests
import json
import re
import time
import datetime
from items import SkuItem
from urllib import parse
from fake_useragent import UserAgent

class YouLeGouSkuFetcher(spider.Fetcher):
    """
    fetcher module, only rewrite url_fetch()
    """
    def url_fetch(self, priority: int, url: str, keys: dict, deep: int, repeat: int, proxies=None):

        time.sleep(1)
        # urls = url.split(',')
        if repeat > 5:
            # print(url)
            time.sleep(5)
        #     return -1, False, None
        proxies = {
                "http": proxies,
                "https": proxies,
        }
        ua = UserAgent()
        headers = {"User-Agent": ua.random}

        try:
            main_response = requests.get(url, proxies=proxies, timeout= 3,headers = headers)
            if main_response.status_code != 200:
                return 0, False, None
            # print(main_response.text)
            return 1, True, main_response.text

        except Exception as e:
            # print(url,e)
            # print('加载超时，重新写入Queue')
            return 0, False, None


class YouLeGouSkuParser(spider.Parser):
    """
    parser module, only rewrite htm_parse()
    """
    def htm_parse(self, priority: int, url: str, keys: dict, deep: int, content: object):
        #
        #
        item = SkuItem()

        item['website'] = [str(keys['Website'])]
        item['productInnerId'] = [str(keys['productInnerId'])]
        item['productURL'] = [str(url)]

        item['productActualID'] = re.compile(r"(?<=listId = \').+?(?=\')").findall(content)
        item['productName'] = re.compile(r"(?<=listName = \').+?(?=\')").findall(content) + re.compile(r"(?<=<h1>).+?(?=<)").findall(content)
        item['brand'] = re.compile(r"(?<=brandName: ').+?(?=')").findall(content)
        item['factoryName'] = re.compile(r"(?<=merchantName = ').+?(?=')").findall(content)
        item['deliveryStartArea'] = re.compile(r"(?<=\"fArea\">)([\s\S]*?)(?=</span>)").findall(content)
        item['productPromPrice'] = re.compile(r"(?<=salePrice: ').+?(?=')").findall(content)
        item['productPrice'] = re.compile(r"(?<=maxPrice: ').+?(?=')").findall(content) + re.compile(r"(?<=salPrice=').+?(?=')").findall(content)
        item['weight'] = re.compile(r"(?<=weight =').+?(?=')").findall(content)
        item['commentCount'] = re.compile(r"(?<=商品评论\(<em>).+?(?=<)").findall(content)

        item['storeActualID'] = re.compile(r"(?<=storeId = ').+?(?=')").findall(content)
        item['storeName'] = re.compile(r"(?<=<a title=\").+?(?=\")").findall(content)
        # item['storeURL'] =
        item['companyName'] = item['factoryName']

        for k, v in item.items():
            item[k] = v[0].strip() if v else ''
        if item['deliveryStartArea'] != '':
            item['deliveryStartArea'] = str(item['deliveryStartArea']).replace('<span>','').strip()

        if item['productActualID']:
            return 1, [], [item]
        else:
            return -1, [], []

class YouLeGouSkuSaver(spider.Saver):

    def __init__(self, config):
        super(YouLeGouSkuSaver,self).__init__(config)
        return


    def item_save(self, url: str, keys: dict, item: (list, tuple)):
        """
        save the item of a url, you can rewrite this function, parameters and return refer to self.working()
        """

        insert_sql = 'insert into data_201806(' + ','.join(item.keys()) + ') VALUES(' + ','.join(['%s' for key in item.keys()]) + ')'
        try:
            self.cursor.execute(insert_sql, tuple(str(item[key]) for key in item.keys()))
            self.db.commit()
        except:
            return -1

        # if self.count % 1000 == 0:
        #     self.db.commit()

        return 1

class YouLeGouSkuProxieser(spider.Proxieser):

    def proxies_get(self):
        url = 'http://127.0.0.1:5010/get_all/?name=YouLeGou_proxy'
        wb_data = requests.get(url)
        # print(wb_data.content)
        proxies = []
        for i in eval(wb_data.text):
            proxies.append(i)
        # print(len(proxies))
        return 0,proxies