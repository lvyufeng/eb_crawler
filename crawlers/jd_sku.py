import spider
import requests
import json
import time
import random
import re
from items import SkuItem

class JingDongSkuFetcher(spider.Fetcher):
    """
    fetcher module, only rewrite url_fetch()
    """
    def url_fetch(self, priority: int, url: str, keys: dict, deep: int, repeat: int, proxies=None):
        urls = url.split(',')
        time.sleep(random.choice((1,2)))
        try:
            proxies = {
                "http": proxies,
                "https": proxies,
            }
            main_response = requests.get(urls[0], proxies=proxies, timeout=5)
            if main_response.status_code != 200:
                return 0, False, None
            comment_response = requests.get(urls[1], proxies=proxies, timeout=5)
            if comment_response.status_code != 200:
                return 0, False, None
            remover = re.compile(r"itemover").findall(main_response.text)
            if remover:
                return -1, False, None


            venderId = re.compile(r"(?<=venderId:).+?(?=,)").findall(main_response.text)
            cat = re.compile(r"(?<=cat: \[).+?(?=\],)").findall(main_response.text)
            if venderId and cat:
                detail_url = urls[2].format(venderId[0],cat[0])
                detail_response = requests.get(detail_url, proxies=proxies, timeout=5)
                if detail_response.status_code != 200:
                    return 0, False, None
                return 1, True, (main_response.text, comment_response.text, detail_response.text)
            elif venderId or cat:
                # print(url)
                return 0, False, None
            else:
                # print(urls[0])
                return -1, False, None
        except Exception as e:
            # print(url,e)
            # print('加载超时，重新写入Queue')
            return 0, False, None


class JingDongSkuParser(spider.Parser):
    """
    parser module, only rewrite htm_parse()
    """
    def htm_parse(self, priority: int, url: str, keys: dict, deep: int, content: object):
        main_text, comment_text, detail_text = content
        detail = json.loads(detail_text)
        temp = comment_text.strip().strip('commentCB(').strip(')')
        comment = json.loads(temp)
        item = SkuItem()

        item['productActualID'] = re.compile(r"(?<=skuid:).+?(?=,)").findall(main_text)
        item['productName'] = re.compile(r"(?<=sku-name\">\n).+?(?=<)").findall(main_text)
        item['weight'] = re.compile(r"(?<=>重量：).+?(?=<)").findall(main_text)
        item['origin'] = re.compile(r"(?<=>商品产地：).+?(?=<)").findall(main_text)
        item['category'] = re.compile(r"(?<=>分类：).+?(?=<)").findall(main_text)
        item['specialtyCategory'] = re.compile(r"(?<=>品种：).+?(?=<)").findall(main_text)
        item['brand'] = re.compile(r"(?<=>品牌：).+?(?=</a>)").findall(main_text)
        item['specification'] = re.compile(r"(?<=>规格：).+?(?=<)").findall(main_text)
        item['deliveryStartArea'] = detail["stock"]["D"]["df"]
        item['productPrice'] = detail["stock"]["jdPrice"]["p"]
        item['productPromPrice'] = detail["stock"]["jdPrice"]["op"]
        item['commentCount'] = comment["result"]["productCommentSummary"]["CommentCount"]

        item['storeActualID'] = detail["stock"]["D"]["vid"]
        item['storeName'] = detail["stock"]["D"]["vender"]
        item['storeURL'] = detail["stock"]["D"]["url"]

        item['companyName'] = item.storeName
        item['storeLocation'] = item.deliveryStartArea

        # item.goodCommentCount
        # url_list = []
        # data = json.loads(html_text)
        # save_list = [data] if data else []
        # print(save_list)

        # return 1, url_list, save_list
        return 1, [], [item]

class JingDongSkuSaver(spider.Saver):

    def item_save(self, url: str, keys: dict, item: (list, tuple)):
        """
        save the item of a url, you can rewrite this function, parameters and return refer to self.working()
        """
        # print(type(item))
        db = self.eb['test_jd']
        db.insert_one(item)
        return 1

class JingDongSkuProxieser(spider.Proxieser):

    def proxies_get(self):
        url = 'http://127.0.0.1:5010/get_all/?name=JingDong_proxy'
        wb_data = requests.get(url)
        # print(wb_data.content)
        proxies = []
        for i in eval(wb_data.text):
            proxies.append(i)
        # print(len(proxies))
        return 0,proxies