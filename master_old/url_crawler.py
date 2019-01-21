import spider
import requests
import json
import time
import random
import datetime
import pymongo
import hashlib
import redis
import re


class UrlFetcher(spider.Fetcher):
    """
    fetcher module, only rewrite url_fetch()
    """
    def url_fetch(self, priority: int, url: str, keys: dict, deep: int, repeat: int, proxies=None):
        headers = {
            'User-Agent': 'android Mozilla/5.0 (Linux; Android 4.4.2; HUAWEI MLA-AL10 Build/HUAWEIMLA-AL10) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36  phh_android_version/3.23.0 phh_android_build',
            # 'Host': 'apiv3.yangkeduo.com'
        }

        if repeat > 1:
        #     # print(url)
            time.sleep(5)
        #     return -1, False, None
        else:
            time.sleep(random.choice((1,0.5)))
        if keys['need_proxy'] == 0:
            proxies = None
        try:
            proxies = {
                "http": proxies,
                "https": proxies,
            }
            response = requests.get(url,headers=headers,proxies=proxies,timeout = 5)

            if response.status_code == 200:
                return 1, keys['need_proxy'] , response.text
            else:
                # print('状态码：{0}'.format(response.status_code), url)
                return 0, -1, None
        except:
            # print('加载超时，重新写入Queue')
                return 0, -1, None


class UrlParser(spider.Parser):
    """
    parser module, only rewrite htm_parse()
    """
    def __init__(self, max_deep=0):
        super(UrlParser, self).__init__(max_deep)

    def htm_parse(self, priority: int, url: str, keys: dict, deep: int, content: object):
        if keys['replace']:
            for i in keys['replace']:
                content = content.replace(i,'')

        data = json.loads(content)

        for i in keys['depth']:
            try:
                data = data[i]
            except:
                return 0, [], []
        url_list = []
        page_num = int(url.split('=')[-1])
        equal = url.rfind('=') + 1
        url_list.append((url[0:equal] + str(page_num+1), keys, priority + 1))
        return 1, url_list, data



        # print(save_list)



class UrlSaver(spider.Saver):


    def __init__(self,config):
        super(UrlSaver, self).__init__(config)
        self.r = redis.Redis.from_url("redis://202.202.5.140:6379", decode_responses=True)
        return


    def item_save(self, url: str, keys: dict, item: (list, tuple)):


        self.r.sadd('sku:'+keys['key'], item)
        return 1

class UrlProxieser(spider.Proxieser):

    def proxies_get(self):
        url = 'http://127.0.0.1:5010/get_all'
        wb_data = requests.get(url)
        # print(wb_data.content)
        proxies = []
        for i in eval(wb_data.text):
            proxies.append(i)
        # print(len(proxies))
        return 0,proxies



