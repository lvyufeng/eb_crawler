import spider
import requests
import json
import re
import time
import datetime
from slave.items import SkuItem
from urllib import parse
import pymongo

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
            # 判断是否是移除或下架产品
            remover = re.compile(r"itemover").findall(content)
            if remover:
                return -1, [], []
            # 获取类别和卖家id
            venderId = re.compile(r"(?<=venderId:).+?(?=,)").findall(content)
            cat = re.compile(r"(?<=cat: \[).+?(?=\],)").findall(content)



            # 解析数据，使用正则表达式解析，返回值为list
            item['website'] = [str(keys['website'])]
            item['keyword'] = [str(keys['keyword'])]
            item['productURL'] = [url]
            item['categoryId'] = cat

            item['productActualID'] = re.compile(r"(?<=skuid:).+?(?=,)").findall(content)
            item['productName'] = re.compile(r"(?<=sku-name\">\n).+?(?=<)").findall(content)
            item['weight'] = re.compile(r"(?<=>重量：).+?(?=<)").findall(content)
            item['origin'] = re.compile(r"(?<=>商品产地：).+?(?=<)").findall(content)
            item['category'] = re.compile(r"(?<=>分类：).+?(?=<)").findall(content)
            item['specialtyCategory'] = re.compile(r"(?<=>品种：).+?(?=<)").findall(content)
            item['brand'] = re.compile(r"(?<= <li title=\').+?(?=\'>品牌)").findall(content)
            item['specification'] = re.compile(r"(?<=>规格：).+?(?=<)").findall(content)
            # 取出list中解析得到的数据
            for k,v in item.items():
                item[k] = v[0].strip() if v else ''
                # 构造评论信息页面url

            keys.update(item)

            # 若存在两者，构造详情信息页面url；
            # 否则返回失败
            if venderId and cat:
                detail_url = 'http://c0.3.cn/stock?skuId=%s' % id + '&area=1_72_4137_0&venderId={}&cat={}&extraParam='.format(
                    venderId[0], cat[0]) + parse.quote('{"originid":"1"}')
                url_list.append((detail_url, keys, priority - 1))
            else:
                return -1, [], []


            return 1, url_list, []


        elif 'commodity' in url:
            # 解析评论信息
            temp = str(content).strip().strip('commentCB(').strip(')')
            comment = json.loads(temp)
            item['commentCount'] = comment["result"]["productCommentSummary"]["CommentCount"]
            item['productActualID'] = str(comment["result"]["productCommentSummary"]["SkuId"])

            # item.update(keys)
            return 1, url_list, [item]


        elif 'stock' in url:
            # 解析详情信息
            detail = json.loads(content)
            item['productActualID'] = str(detail["stock"]["realSkuId"])
            item['productPrice'] = detail["stock"]["jdPrice"]["op"]
            item['productPromPrice'] = detail["stock"]["jdPrice"]["p"]
            # 商户信息存在 detail["stock"]["D"]
            if 'D' in detail["stock"]:
                item['deliveryStartArea'] = detail["stock"]["D"]["df"]
                item['storeActualID'] = detail["stock"]["D"]["vid"]
                item['storeName'] = detail["stock"]["D"]["vender"]
                item['storeURL'] = detail["stock"]["D"]["url"]
                item['companyName'] = detail["stock"]["D"]["vender"]
                item['storeLocation'] = detail["stock"]["D"]["df"]
            # 商户信息存在 detail["stock"]["self_D"]
            elif 'self_D' in detail["stock"]:
                item['deliveryStartArea'] = detail["stock"]["self_D"]["df"]
                item['storeActualID'] = detail["stock"]["self_D"]["vid"]
                item['storeName'] = detail["stock"]["self_D"]["vender"]
                item['storeURL'] = detail["stock"]["self_D"]["url"]

                item['companyName'] = detail["stock"]["self_D"]["vender"]
                item['storeLocation'] = detail["stock"]["self_D"]["df"]
            # 商户信息不存在
            else:
                item['deliveryStartArea'] = None
                item['storeActualID'] = None
                item['storeName'] = None
                item['storeURL'] = None

                item['companyName'] = None
                item['storeLocation'] = None

            keys.update(item)
            comment_url = 'http://wq.jd.com/commodity/comment/getcommentlist?sku=%s' % item['productActualID']
            url_list.append((comment_url, keys, priority - 1))

            return 1, url_list, []

        else:
            # 无效url返回的content
            return -1, [], []



class JingDongSkuSaver(spider.Saver):

    def __init__(self, config):
        super(JingDongSkuSaver,self).__init__(config)
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
        # if 'item' in url:
        #     try:
        #         self.collection.insert_one(item)
        #
        #         # self.count = self.count + 1
        #     except Exception as e:
        #         return -1
        #     # pass
        #
        # else:
        #
        #     try:
        #         self.collection.update({'productActualID': item["productActualID"]}, {'$set': item}, False)
        #
        #         # self.count = self.count + 1
        #     except Exception as e:
        #         return -1

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