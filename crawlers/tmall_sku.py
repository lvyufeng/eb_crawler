import spider
import requests
import json
import time
import random
from urllib import parse
from items import SkuItem
import datetime
import pymongo

class TmallSkuFetcher(spider.Fetcher):
    """
    fetcher module, only rewrite url_fetch()
    """
    def url_fetch(self, priority: int, url: str, keys: dict, deep: int, repeat: int, proxies=None):

        if repeat > 5:
        #     # print(url)
            time.sleep(5)
        #     return -1, False, None
        else:
            time.sleep(random.choice((1,0.5)))
        id = url.split('=')[-1]
        url = 'http://h5api.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0/?data=' + parse.quote('{"exParams":"{\"id\":\"' + id + '\"}","itemNumId":"' + id + '"}')

        try:
            proxies = {
                "http": proxies,
                "https": proxies,
            }

            response = requests.get(url, proxies=proxies,timeout = 5)

            if response.status_code == 200:
                data = json.loads(response.text)
                if 'SUCCESS' in data['ret'][0]:
                    return 1, True, (response.text, response.url, proxies)
                else:
                    # print('爬取失败，重新写入Queue')
                    return 0, False, None
            elif response.status_code != 204:
                # print('服务器错误')
                return 0, False, None
            else:
                # print('状态码：{0}'.format(response.status_code), url)

                return -1, False, None
        except:
            # print('加载超时，重新写入Queue')
            return 0, False, None


class TmallSkuParser(spider.Parser):
    """
    parser module, only rewrite htm_parse()
    """
    def htm_parse(self, priority: int, url: str, keys: dict, deep: int, content: object):
        response_text, response_url, proxies = content
        url_list = []
        item = SkuItem()
        try:
            data = json.loads(response_text)
        except:
            return -1,[],[]
        if 'SUCCESS' in data['ret'][0]:
            if 'item' in data['data']:
                try:
                    value = json.loads(data['data']['apiStack'][0]['value'])
                except:
                    return -1,[],[]
                item['website'] = keys['website']
                item['keyword'] = keys['keyword']
                item['productURL'] = url
                item['categoryId'] = data['data']['item']['rootCategoryId'] if 'itemId' in data['data']['item'] else None
                # 链接
                item['productActualID'] = data['data']['item']['itemId'] if 'itemId' in data['data']['item'] else None

                item['productName'] = data['data']['item']['title'] if 'title' in data['data']['item'] else None
                # 商品名称
                item['productDescription'] = data['data']['item']['subtitle'] if 'subtitle' in data['data']['item'] else None

                if data['data']['props']:
                    for i in data['data']['props']['groupProps'][0]['基本信息']:
                        if '净含量' in list(i.keys()):
                            item['weight'] = i['净含量']
                        if '产地' in list(i.keys()):
                            item['origin'] = i['产地']
                        if '省份' in list(i.keys()):
                            item['province'] = i['省份']
                        if '城市' in list(i.keys()):
                            item['city'] = i['城市']
                        if '种类' in list(i.keys()):
                            item['category'] = i['种类']
                        if '品类' in list(i.keys()):
                            item['specialtyCategory'] = i['品类']
                        if '品牌' in list(i.keys()):
                            item['brand'] = i['品牌']
                        if '厂名' in list(i.keys()):
                            item['factoryName'] = i['厂名']
                        if '厂址' in list(i.keys()):
                            item['factoryAddress'] = i['厂址']
                        if '系列' in list(i.keys()):
                            item['series'] = i['系列']

                if 'extraPrices' in value['price']:
                    item['productPrice'] = value['price']['extraPrices'][0]['priceText'] if value['price']['extraPrices'] else None

                    item['productPromPrice'] = value['price']['price']['priceText']
                else:
                    item['productPrice'] = value['price']['price']['priceText']
                            # 商品原始价格
                    item['productPromPrice'] = None
                # 促销价格
                item['monthSaleCount'] = value['item']['sellCount'] if 'sellCount' in value['item'] else None
                # item['monthSaleCount'] = value['item']['sellCount']
                item['deliveryStartArea'] = value['delivery']['from'] if 'from' in value['delivery'] else None
                    # 月销量
                item['commentCount'] = data['data']['item']['commentCount'] if 'commentCount' in data['data']['item'] else None
                    # 评论数量
                item['storeActualID'] = data['data']['seller']['shopId'] if 'shopId' in data['data']['seller'] else None
                    # 平台中店铺的编号
                item['storeName'] = data['data']['seller']['shopName'] if 'shopName' in data['data']['seller'] else None

                    # 店铺名称
                item['storeURL'] = data['data']['seller']['taoShopUrl'] if 'taoShopUrl' in data['data']['seller'] else None

                    # 店铺链接
                item['shopkeeper'] = data['data']['seller']['sellerNick'] if 'sellerNick' in data['data']['seller'] else None

                # item['errorInfo'] = value['trade']['hintBanner']['text'] if 'hintBanner' in value['trade'] else None
            else:
                return -1, [], []

        else:
            return -1, [], []
        # print(save_list)

        return 1, url_list, [item]

class TmallSkuSaver(spider.Saver):

    def __init__(self, config):
        super(TmallSkuSaver,self).__init__(config)
        client = pymongo.MongoClient(self.cf.getStr('mongodb', 'db_host'), self.cf.getInt('mongodb', 'db_port'))
        db = client['test']
        self.collection = db['data_' + datetime.datetime.now().strftime('%Y%m')]
        return

    def item_save(self, url: str, keys: dict, item: (list, tuple)):
        """
        save the item of a url, you can rewrite this function, parameters and return refer to self.working()
        """
        # print(type(item))
        item.update(keys)

        self.collection.update({'productActualID': item["productActualID"]}, {'$set': item}, True)
        return 1

class TmallSkuProxieser(spider.Proxieser):

    def proxies_get(self):
        url = 'http://127.0.0.1:5010/get_all/?name=TaoBao_proxy'
        wb_data = requests.get(url)
        # print(wb_data.content)
        proxies = []
        for i in eval(wb_data.text):
            proxies.append(i)
        # print(len(proxies))
        return 0,proxies



