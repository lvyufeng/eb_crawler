import spider
import requests
import json
import re
import time
import datetime
from items import SkuItem
from urllib import parse
import pymongo

class BaiduMapFetcher(spider.Fetcher):
    """
    fetcher module, only rewrite url_fetch()
    """
    def url_fetch(self, priority: int, url: str, keys: dict, deep: int, repeat: int, proxies=None):

        try:
            main_response = requests.get(url)
            if main_response.status_code != 200:
                return 0, False, None
            # print(main_response.text)
            return 1, True, main_response.text

        except Exception as e:
            # print(url,e)
            # print('加载超时，重新写入Queue')
            return 0, False, None


class BaiduMapParser(spider.Parser):
    """
    parser module, only rewrite htm_parse()
    """
    def htm_parse(self, priority: int, url: str, keys: dict, deep: int, content: object):
        #
        #
        data = json.loads(content)

        return 1, [], [data]

class BaiduMapSaver(spider.Saver):

    def __init__(self, config):
        super(BaiduMapSaver,self).__init__(config)
        self.count = 0
        self.db = pymongo.MongoClient('localhost',27017)
        self.baidumap = self.db['baidumap']
        self.result = self.baidumap['result']
        self.cursor = None
        return


    def item_save(self, url: str, keys: dict, item: (list, tuple)):
        """
        save the item of a url, you can rewrite this function, parameters and return refer to self.working()
        """

        self.result.insert(item)
        return 1
