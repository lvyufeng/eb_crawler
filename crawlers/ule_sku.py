import spider
import requests
import json
import re
import time
import datetime
from items import SkuItem
from urllib import parse

class JingDongSkuFetcher(spider.Fetcher):
    """
    fetcher module, only rewrite url_fetch()
    """
    def url_fetch(self, priority: int, url: str, keys: dict, deep: int, repeat: int, proxies=None):


        # urls = url.split(',')
        if repeat > 5:
            # print(url)
            time.sleep(5)
            return -1, False, None
        proxies = {
                "http": proxies,
                "https": proxies,
        }
        try:
            main_response = requests.get(url, proxies=proxies, timeout= 3)
            if main_response.status_code != 200:
                return 0, False, None
            # print(main_response.text)
            return 1, True, main_response.text

        except Exception as e:
            # print(url,e)
            # print('加载超时，重新写入Queue')
            return 0, False, None


class JingDongSkuParser(spider.Parser):
    """
    parser module, only rewrite htm_parse()
    """
    def htm_parse(self, priority: int, url: str, keys: dict, deep: int, content: object):
        #
        #
        item = SkuItem()
        url_list = []
        #
        if 'item' in url:
            id = url.split('/')[-1].split('.')[0]
            remover = re.compile(r"itemover").findall(content)
            if remover:
                return -1, [], []
            venderId = re.compile(r"(?<=venderId:).+?(?=,)").findall(content)
            cat = re.compile(r"(?<=cat: \[).+?(?=\],)").findall(content)
            if venderId and cat:
                detail_url = 'http://c0.3.cn/stock?skuId=%s' %id +'&area=1_72_4137_0&venderId={}&cat={}&extraParam='.format(venderId[0], cat[0]) + parse.quote('{"originid":"1"}')
                url_list.append((detail_url, keys, priority-1))
            else:
                return -1, [], []
            comment_url = 'http://wq.jd.com/commodity/comment/getcommentlist?sku=%s' %id
            url_list.append((comment_url, keys, priority-1))

            item['productActualID'] = int(re.compile(r"(?<=skuid:).+?(?=,)").findall(content)[0])
            item['productName'] = re.compile(r"(?<=sku-name\">\n).+?(?=<)").findall(content)
            item['weight'] = re.compile(r"(?<=>重量：).+?(?=<)").findall(content)
            item['origin'] = re.compile(r"(?<=>商品产地：).+?(?=<)").findall(content)
            item['category'] = re.compile(r"(?<=>分类：).+?(?=<)").findall(content)
            item['specialtyCategory'] = re.compile(r"(?<=>品种：).+?(?=<)").findall(content)
            item['brand'] = re.compile(r"(?<=>品牌：).+?(?=</a>)").findall(content)
            item['specification'] = re.compile(r"(?<=>规格：).+?(?=<)").findall(content)

        elif 'commodity' in url:
            # print(content)
            temp = str(content).strip().strip('commentCB(').strip(')')
            comment = json.loads(temp)
            item['commentCount'] = comment["result"]["productCommentSummary"]["CommentCount"]
            item['productActualID'] = comment["result"]["productCommentSummary"]["SkuId"]


        elif 'stock' in url:
            detail = json.loads(content)
            item['productActualID'] = detail["stock"]["realSkuId"]
            item['productPrice'] = detail["stock"]["jdPrice"]["op"]
            item['productPromPrice'] = detail["stock"]["jdPrice"]["p"]
            try:
                item['deliveryStartArea'] = detail["stock"]["D"]["df"] if 'D' in detail["stock"] else \
                    detail["stock"]["self_D"]["df"]
                item['storeActualID'] = detail["stock"]["D"]["vid"] if 'D' in detail["stock"] else \
                detail["stock"]["self_D"]["vid"]
                item['storeName'] = detail["stock"]["D"]["vender"] if 'D' in detail["stock"] else detail["stock"]["self_D"][
                    "vender"]
                item['storeURL'] = detail["stock"]["D"]["url"] if 'D' in detail["stock"] else detail["stock"]["self_D"][
                    "url"]

                item['companyName'] = detail["stock"]["D"]["vender"] if 'D' in detail["stock"] else \
                detail["stock"]["self_D"]["vender"]
                item['storeLocation'] = detail["stock"]["D"]["df"] if 'D' in detail["stock"] else detail["stock"]["self_D"]["df"]
            except:
                item['deliveryStartArea'] = None
                item['storeActualID'] = None
                item['storeName'] = None
                item['storeURL'] = None

                item['companyName'] = None
                item['storeLocation'] = None


        else:
            return -1, [], []

        return 1, url_list, [item]

class JingDongSkuSaver(spider.Saver):

    def __init__(self, config):
        super(JingDongSkuSaver,self).__init__(config)
        self.db = self.eb['JingDong_' + str(datetime.datetime.now().month)]
        return


    def item_save(self, url: str, keys: dict, item: (list, tuple)):
        """
        save the item of a url, you can rewrite this function, parameters and return refer to self.working()
        """
        # print(type(item))

        self.db.update({'productActualID': item["productActualID"]}, {'$set': item},True)
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