import spider
import requests
import time
import random
import datetime
import re
import pymongo

class SuNingUrlFetcher(spider.Fetcher):
    """
    fetcher module, only rewrite url_fetch()
    """
    def url_fetch(self, priority: int, url: str, keys: dict, deep: int, repeat: int, proxies=None):

        if repeat > 1:
        #     # print(url)
            time.sleep(5)
        #     return -1, False, None
        else:
            time.sleep(random.choice((1,0.5)))
        try:
            proxies = {
                "http": proxies,
                "https": proxies,
            }
            response = requests.get(url, proxies=proxies,timeout = 2)

            if response.status_code == 200:

                return 1, True, response.text

            else:
                # print('状态码：{0}'.format(response.status_code), url)

                return -1, False, None
        except:
            # print('加载超时，重新写入Queue')
            return 0, False, None


class SuNingUrlParser(spider.Parser):
    """
    parser module, only rewrite htm_parse()
    """
    def htm_parse(self, priority: int, url: str, keys: dict, deep: int, content: object):
        response_text = content
        url_list = []
        sku_list = []

        # item = SkuItem()


        no_result = re.compile(r"(?<=没有找到).+?(?=)").findall(content)
        #no-result-tips
        if no_result:
            return -1,[],[]

        list = re.compile(r"(?<=href=\"//).+?(?=\"class=\"sellPoint\")").findall(content)
        # href="/%E8%8B%B9%E6%9E%9C/&amp;iy=0&amp;cp=49" id="nextPage"
        next = re.compile(r"(?<=href=\").+?(?=\"id=\"nextPage\")").findall(content)
        for i in next:
            if 'cp=' in i and 'cp=1' not in i:
                url_list.append(('http://search.suning.com' + i, keys, priority + 1))
        for i in list:
            sku_list.append({
                '_id': 's' + str(i).split('.')[-2].replace('com/','')
            })
        # item = SkuItem()
        return 1, url_list, sku_list

class SuNingUrlSaver(spider.Saver):


    def __init__(self):
        self.count = 0
        client = pymongo.MongoClient('localhost')
        db = client['sku']
        self.collection = db['sku_ids_' + datetime.datetime.now().strftime('%Y%m')]
        return


    def item_save(self, url: str, keys: dict, item: (list, tuple)):
        """
        save the item of a url, you can rewrite this function, parameters and return refer to self.working()
        """
        item.update(keys)
        # pass
        try:
            self.collection.insert(item)
        except:
            return -1

        # if self.count % 1000 == 0:
        #     self.db.commit()

        return 1

class SuNingUrlProxieser(spider.Proxieser):

    def proxies_get(self):
        url = 'http://127.0.0.1:5010/get_all/?name=SuNing_proxy'
        wb_data = requests.get(url)
        # print(wb_data.content)
        proxies = []
        for i in eval(wb_data.text):
            proxies.append(i)
        # print(len(proxies))
        return 0,proxies

