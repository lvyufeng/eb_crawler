import spider
import requests
import json
import time
import random
import datetime
import pymongo
import redis

class YouLeGouUrlFetcher(spider.Fetcher):
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


class YouLeGouUrlParser(spider.Parser):
    """
    parser module, only rewrite htm_parse()
    """
    def htm_parse(self, priority: int, url: str, keys: dict, deep: int, content: object):
        response_text = content
        url_list = []
        sku_list = []
        # item = SkuItem()
        try:
            data = json.loads(response_text)
            if 'resultList' not in data:
                return 1, url_list, sku_list

            for i in data['resultList']:
                sku_list.append({
                    '_id': str(i['listingId']),
                    'keyword': keys['keyword'],
                    'website': keys['website']

                })
            pass

            next_page = int(url.split('=')[-1]) + 1
            url_list.append((url.replace('pageIndex='+url.split('=')[-1],'pageIndex='+str(next_page)), keys, priority + 1))

            return 1, url_list, sku_list
        except Exception as e:
            pass
            return -1,[],[]

        # print(save_list)

        # return 1, url_list, [item]

class YouLeGouUrlSaver(spider.Saver):


    def __init__(self):
        self.count = 0
        client = pymongo.MongoClient('localhost')
        db = client['sku']
        self.collection = db['sku_ids_' + datetime.datetime.now().strftime('%Y%m')]
        self.r = redis.Redis.from_url("redis://202.202.5.140:6379", decode_responses=True)
        return


    def item_save(self, url: str, keys: dict, item: (list, tuple)):
        """
        save the item of a url, you can rewrite this function, parameters and return refer to self.working()
        """
        # item.update(keys)
        # pass
        try:
            self.collection.insert(item)
        except:
            return -1
        self.r.sadd('sku:' + keys['website'], item)
        # if self.count % 1000 == 0:
        #     self.db.commit()

        return 1

class YouLeGouUrlProxieser(spider.Proxieser):

    def proxies_get(self):
        url = 'http://127.0.0.1:5010/get_all/?name=YouLeGou_proxy'
        wb_data = requests.get(url)
        # print(wb_data.content)
        proxies = []
        for i in eval(wb_data.text):
            proxies.append(i)
        # print(len(proxies))
        return 0,proxies

