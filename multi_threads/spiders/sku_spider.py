import sys
from threading import Thread
import json
sys.path.append('../')
import random
import requests
import json
from utils.get_proxy import GetAllIPs
import pymongo
import datetime

class skuSpider(Thread):
    def __init__(self,queue,config):
        Thread.__init__(self)
        self.queue = queue
        self.proxies = GetAllIPs()
        self.client = pymongo.MongoClient('localhost', 27017)
        # client = pymongo.MongoClient('localhost',27017)
        self.eb = self.client['test']
        self.db = self.eb[platform + '_' + str(datetime.datetime.now().month)]
        # self.db = self.eb['tmall_06']
        self.proxies_len = len(self.proxies)/2

    def run(self):
        while self.queue.qsize():
            url = self.queue.get()
            proxy = random.choice(self.proxies)
            proxies = {
                        "http": proxy,
                        "https": proxy,
                    }
            try:
                wb_data = requests.get(url, proxies=proxies, timeout=3)
                if wb_data.status_code == 200:
                    data = json.loads(wb_data.text)
                    if 'SUCCESS' in data['ret'][0]:
                        data = json.loads(wb_data.text)
                        # pass
                        self.db.insert_one(data)
                        print('爬取成功')
                    else:
                        if len(self.proxies) > self.proxies_len:
                            self.proxies.remove(proxy)
                            print('代理{0}失效'.format(proxy))
                        else:
                            self.proxies = GetAllIPs()
                            print('代理不足，重新获取')
                            # self.queue.put(url)
                        self.queue.put(url)
                        print('爬取失败，重新写入Queue')
                elif wb_data.status_code != 204:
                    print('服务器错误')
                    self.queue.put(url)
                else:
                    print('状态码：{0}'.format(wb_data.status_code),url)
            except:
                self.queue.put(url)
                if len(self.proxies) > self.proxies_len:
                    self.proxies.remove(proxy)
                    # print()
                    print('加载超时，重新写入Queue，代理{0}失效'.format(proxy))
                else:
                    self.proxies = GetAllIPs()
                    print('加载超时，重新写入Queue，代理不足，重新获取')

            self.queue.task_done()