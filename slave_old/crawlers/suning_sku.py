import spider
import requests
import json
import time
import re
import datetime
from slave_old.items import SkuItem
import pymongo

class SuNingSkuFetcher(spider.Fetcher):
    """
    fetcher module, only rewrite url_fetch()
    """
    def url_fetch(self, priority: int, url: str, keys: dict, deep: int, repeat: int, proxies=None):

        if repeat > 0:
            time.sleep(5)
        else:
            time.sleep(1)
        proxies = {
                "http": proxies,
                "https": proxies,
        }
        try:
            main_response = requests.get(url, proxies=proxies, timeout= 3)
            if main_response.status_code == 218 or main_response.status_code == 404:
                return -1, False, None

            if main_response.status_code != 200:
                return 0, False, None
            # print(main_response.text)
            return 1, True, main_response.text

        except Exception as e:
            # print(url,e)
            # print('加载超时，重新写入Queue')
            return 0, False, None

class SuNingSkuParser(spider.Parser):
    """
    parser module, only rewrite htm_parse()
    """
    def htm_parse(self, priority: int, url: str, keys: dict, deep: int, content: object):
        '''

        :param priority:
        :param url:
        :param keys:
        :param deep:
        :param content:
        :return:
        '''
        item = SkuItem()
        url_list = []
        #
        if 'product' in url:
            # re.compile(r'其它类似商品').findall(content) or
            if re.compile(r'对不起，您浏览的商品暂时无法显示').findall(content) or re.compile(r'苏宁易购电子书').findall(content):
                return -1, [], []

            # if len(url.split('/')) == 4:
            #     return -1, [], []


            item['productActualID'] = re.compile(r"(?<=ninePartNumber\":\").+?(?=\")").findall(content)
            item['productCompleteID'] = re.compile(r"(?<=\"partNumber\":\").+?(?=\")").findall(content)
            item['storeActualID'] = re.compile(r"(?<=vendorCode\":\").+?(?=\")").findall(content)


            item['website'] = [str(keys['website'])]
            item['keyword'] = [keys['keyword']]
            item['productURL'] = [url]

            item['productName'] = re.compile(r"(?<=\"itemDisplayName\":\").+?(?=\")").findall(content)
            item['weight'] = re.compile(r"(?<=净含量</span> </div> </td> <td class=\"val\">).+?(?=<)").findall(content)
            item['origin'] = re.compile(r"(?<=产地：).+?(?=<)").findall(content)
            item['category'] = re.compile(r"(?<=类别：).+?(?=<)").findall(content)
            item['category1'] = re.compile(r"(?<=categoryName1\":\").+?(?=\")").findall(content)
            item['categoryId'] = re.compile(r"(?<=category1\":\").+?(?=\")").findall(content)
            item['category2'] = re.compile(r"(?<=categoryName2\":\").+?(?=\")").findall(content)
            item['category3'] = re.compile(r"(?<=categoryName3\":\").+?(?=\")").findall(content)
            item['brand'] = re.compile(r"(?<=品牌：).+?(?=</span>)").findall(content)
            item['expirationDay'] = re.compile(r"(?<=保质期</span> </div> </td> <td class=\"val\">).+?(?=<)").findall(content)

            # 取出list中解析得到的数据
            for k, v in item.items():
                item[k] = v[0].strip() if v else ''

            keys.update(item)
            if int(url.split('/')[-2]) != 0:
                shop_url = 'http://shop.suning.com/jsonp/{}/shopinfo/shopinfo.html'.format(int(url.split('/')[-2]))
                url_list.append((shop_url, keys, priority-1))

                return 1, url_list, []
            elif item['productCompleteID'] and item['storeActualID'] :
                pas_url = 'http://pas.suning.com/nspcsale_0_{}_{}_{}_320_023_0230101_500353_1000333_9325_12583_Z001___R9006371.html'.format(keys['productCompleteID'], keys['productCompleteID'], keys['storeActualID'])
                url_list.append((pas_url, keys, priority - 1))
                    # url_list.append((review_url, {'productActualID':item['productActualID'][0]}, priority-1))
                return 1, url_list, []
            else:
                return -1, [], []

        elif 'shop' in url:
            item['productActualID'] = keys['productActualID']
            shop = json.loads(str(content).strip().strip('shopinfo(').strip(')'))
            item['storeName'] = shop['shopName']
            item['storeURL'] = shop['shopDomain']
            item['storeLocation'] = shop['companyAddress']
            item['companyName'] = shop['companyName']


            keys.update(item)

            if keys['productCompleteID'] and keys['storeActualID'] :
                pas_url = 'http://pas.suning.com/nspcsale_0_{}_{}_{}_320_023_0230101_500353_1000333_9325_12583_Z001___R9006371.html'.format(keys['productCompleteID'],keys['productCompleteID'],keys['storeActualID'])
                # review_url = 'http://review.suning.com/ajax/cluster_review_satisfy/general--{}-{}-----satisfy.htm'.format(item['productCompleteID'][0],url.split('/')[-2])
                url_list.append((pas_url, keys, priority-1))
                # url_list.append((review_url, {'productActualID':item['productActualID'][0]}, priority-1))
                return 1, url_list, []
            else:
                return -1, [], []

            pass

        elif 'pas' in url:
            item['productActualID'] = keys['productActualID']
            pas = json.loads(str(content).strip().strip('pcData(').strip(')'))
            item['productPrice'] = pas['data']['price']['saleInfo'][0]['netPrice']
            item['productPromPrice'] = pas['data']['price']['saleInfo'][0]['promotionPrice']
            # pcData(
            # pass

            keys.update(item)

            if keys['productCompleteID'] and keys['storeActualID']:
                review_url = 'http://review.suning.com/ajax/cluster_review_satisfy/general--{}-{}-----satisfy.htm'.format(keys['productCompleteID'],keys['storeActualID'])
                url_list.append((review_url, keys, priority-1))
                return 1, url_list, []
            else:
                return -1, [], []
        elif 'review' in url:
            item['productActualID'] = keys['productActualID']
            review = json.loads(str(content).strip().strip('satisfy(').strip(')'))
            item['commentCount'] = review['reviewCounts'][0]['totalCount']
            # pass

            return 1, url_list, [item]
        else:
            return -1, [], []

        # return 1, url_list, [item]

        # self.shopId = re.compile(r"(?<=shopid=).+?(?=;)").findall(self.main_response.text)
        #
        # if self.shopId:
        #     if self.shopId[0] != '0000000000':
        #         shop_url = urls[1].format(shopId[0].strip('"'))
        #         shop_response = requests.get(shop_url, proxies=proxies, timeout=5)
        #         if shop_response.status_code != 200:
        #             return 0, False, None
        # else:
        #     return -1, False, None
        # partNumber = re.compile(r"(?<=passPartNumber\":\").+?(?=\")").findall(main_response.text)
        # if partNumber:
        #     nspcsale_url = urls[2].format(partNumber[0], partNumber[0], shopId[0])
        #     nspcsale_response = requests.get(nspcsale_url, proxies=proxies, timeout=5)
        #     if nspcsale_response.status_code != 200:
        #         return 0, False, None

class SuNingSkuSaver(spider.Saver):

    def __init__(self, config):
        super(SuNingSkuSaver,self).__init__(config)
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
        try:
            self.collection.insert_one(item)

            # self.count = self.count + 1
        except Exception as e:
            return -1


        # if 'product' in url:
        #     self.collection.insert_one(item)
        #
        # else:
        #     try:
        #         self.collection.update({'productActualID': item["productActualID"]}, {'$set': item}, False)
        #         # self.count = self.count + 1
        #     except Exception as e:
        #         return -1

        return 1


class SuNingSkuProxieser(spider.Proxieser):

    def proxies_get(self):
        url = 'http://127.0.0.1:5010/get_all/?name=SuNing_proxy'
        wb_data = requests.get(url)
        # print(wb_data.content)
        proxies = []
        for i in eval(wb_data.text):
            proxies.append(i)
        # print(len(proxies))
        return 0,proxies