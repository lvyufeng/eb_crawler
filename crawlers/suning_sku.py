import spider
import requests
import json
import time
import random
import re
import datetime
from items import SkuItem

class SuNingSkuFetcher(spider.Fetcher):
    """
    fetcher module, only rewrite url_fetch()
    """
    def url_fetch(self, priority: int, url: str, keys: dict, deep: int, repeat: int, proxies=None):
        self.urls = url.split(',')
        self.proxies = {
            "http": proxies,
            "https": proxies,
        }
        time.sleep(random.choice((1,2)))
        try:

            self.main_response = requests.get(self.urls[0], proxies=self.proxies, timeout=5)
            if self.main_response.status_code != 200:
                return 0, False, None
            self.shopId = re.compile(r"(?<=shopid=).+?(?=;)").findall(self.main_response.text)

            if self.shopId:
                if self.shopId[0] != '0000000000':
                    shop_url = urls[1].format(shopId[0].strip('"'))
                    shop_response = requests.get(shop_url,proxies=proxies, timeout=5)
                    if shop_response.status_code != 200:
                        return 0, False, None
            else:
                return -1, False, None
            partNumber = re.compile(r"(?<=passPartNumber\":\").+?(?=\")").findall(main_response.text)
            if partNumber:
                nspcsale_url = urls[2].format(partNumber[0],partNumber[0], shopId[0])
                nspcsale_response = requests.get(nspcsale_url, proxies=proxies, timeout=5)
                if nspcsale_response.status_code != 200:
                    return 0, False, None

            # comment_response = requests.get(urls[1], proxies=proxies, timeout=5)
            # if comment_response.status_code != 200:
            #     return 0, False, None
            # remover = re.compile(r"itemover").findall(main_response.text)
            # if remover:
            #     return -1, False, None
            #
            #
            # cat = re.compile(r"(?<=cat: \[).+?(?=\],)").findall(main_response.text)
            # if venderId and cat:
            #     detail_url = urls[2].format(venderId[0],cat[0])
            #     detail_response = requests.get(detail_url, proxies=proxies, timeout=5)
            #     if detail_response.status_code != 200:
            #         return 0, False, None
            #     return 1, True, (main_response.text, comment_response.text, detail_response.text)
            # elif venderId or cat:
            #     # print(url)
            #     return 0, False, None
            # else:
            #     # print(urls[0])
            #     return -1, False, None
        except Exception as e:
            # print(url,e)
            # print('加载超时，重新写入Queue')
            return 0, False, None


class SuNingSkuParser(spider.Parser):
    """
    parser module, only rewrite htm_parse()
    """
    def htm_parse(self, priority: int, url: str, keys: dict, deep: int, content: object):
        main_text, comment_text, detail_text = content
        # detail = json.loads(detail_text)
        # temp = comment_text.strip().strip('commentCB(').strip(')')
        # comment = json.loads(temp)
        # item = SkuItem()
        #
        # item['productActualID'] = re.compile(r"(?<=skuid:).+?(?=,)").findall(main_text)
        # item['productName'] = re.compile(r"(?<=sku-name\">\n).+?(?=<)").findall(main_text)
        # item['weight'] = re.compile(r"(?<=>重量：).+?(?=<)").findall(main_text)
        # item['origin'] = re.compile(r"(?<=>商品产地：).+?(?=<)").findall(main_text)
        # item['category'] = re.compile(r"(?<=>分类：).+?(?=<)").findall(main_text)
        # item['specialtyCategory'] = re.compile(r"(?<=>品种：).+?(?=<)").findall(main_text)
        # item['brand'] = re.compile(r"(?<=>品牌：).+?(?=</a>)").findall(main_text)
        # item['specification'] = re.compile(r"(?<=>规格：).+?(?=<)").findall(main_text)
        # item['deliveryStartArea'] = detail["stock"]["D"]["df"] if 'D' in detail["stock"] else detail["stock"]["self_D"]["df"]
        # item['productPrice'] = detail["stock"]["jdPrice"]["p"]
        # item['productPromPrice'] = detail["stock"]["jdPrice"]["op"]
        # item['commentCount'] = comment["result"]["productCommentSummary"]["CommentCount"]
        #
        # item['storeActualID'] = detail["stock"]["D"]["vid"] if 'D' in detail["stock"] else detail["stock"]["self_D"]["vid"]
        # item['storeName'] = detail["stock"]["D"]["vender"] if 'D' in detail["stock"] else detail["stock"]["self_D"]["vender"]
        # item['storeURL'] = detail["stock"]["D"]["url"] if 'D' in detail["stock"] else detail["stock"]["self_D"]["url"]
        #
        # item['companyName'] = detail["stock"]["D"]["vender"] if 'D' in detail["stock"] else detail["stock"]["self_D"]["vender"]
        # item['storeLocation'] = detail["stock"]["D"]["df"] if 'D' in detail["stock"] else detail["stock"]["self_D"]["df"]

        # item.goodCommentCount
        # url_list = []
        # data = json.loads(html_text)
        # save_list = [data] if data else []
        # print(save_list)

        # return 1, url_list, save_list
        return 1, [], []

class SuNingSkuSaver(spider.Saver):

    def item_save(self, url: str, keys: dict, item: (list, tuple)):
        """
        save the item of a url, you can rewrite this function, parameters and return refer to self.working()
        """
        # print(type(item))
        db = self.eb['suning_' + str(datetime.datetime.now().month)]
        db.insert_one(item)
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