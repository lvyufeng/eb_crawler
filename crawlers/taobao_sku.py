import spider
import requests
import json
import time
import random
from urllib import parse
from items import SkuItem

class TaoBaoSkuFetcher(spider.Fetcher):
    """
    fetcher module, only rewrite url_fetch()
    """
    def url_fetch(self, priority: int, url: str, keys: dict, deep: int, repeat: int, proxies=None):
        time.sleep(random.choice((1,2)))
        id = url.split('=')[-1]
        url = 'http://h5api.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0/?data=' + parse.quote('{"exParams":"{\"id\":\"' + id + '\"}","itemNumId":"' + id + '"}')
        try:
            proxies = {
                "http": proxies,
                "https": proxies,
            }
            response = requests.get(url, proxies=proxies,timeout = 2)

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


class TaoBaoSkuParser(spider.Parser):
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
                value = json.loads(data['data']['apiStack'][0]['value'])
                item['website'] = keys['Website']
                item['productInnerId'] = keys['productInnerId']
                item['productURL'] = url
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
                item['monthSaleCount'] = value['item']['sellCount']
                item['deliveryStartArea'] = value['delivery']['from']
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
                return 0, [(url, keys, priority)], []

        else:
            return 0,[(url, keys, priority)],[]
        # print(save_list)

        return 1, url_list, [item]

class TaoBaoSkuSaver(spider.Saver):

    def __init__(self, config):
        super(TaoBaoSkuSaver,self).__init__(config)
        self.count = 0
        return


    def item_save(self, url: str, keys: dict, item: (list, tuple)):
        """
        save the item of a url, you can rewrite this function, parameters and return refer to self.working()
        """

        insert_sql = 'insert into data_201806(' + ','.join(item.keys()) + ') VALUES(' + ','.join(['%s' for key in item.keys()]) + ')'
        try:
            self.cursor.execute(insert_sql, tuple(str(item[key]) for key in item.keys()))
            self.count = self.count + 1
        except:
            pass

        if self.count % 1000 == 0:
            self.db.commit()

        return 1

class TaoBaoSkuProxieser(spider.Proxieser):

    def proxies_get(self):
        url = 'http://127.0.0.1:5010/get_all/?name=TaoBao_proxy'
        wb_data = requests.get(url)
        # print(wb_data.content)
        proxies = []
        for i in eval(wb_data.text):
            proxies.append(i)
        # print(len(proxies))
        return 0,proxies



