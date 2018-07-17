import sys
from threading import Thread
import json
import random
import requests
import json
from utils.get_proxy import GetAllIPs
import pymongo
import datetime

class urlSpider(Thread):
    def __init__(self,queue,set,eb,config):
        Thread.__init__(self)
        self.queue = queue
        # self.proxies = GetAllIPs()

        # self.db = self.eb['product_info']
        self.db = eb['url_test']
        self.url_set = set()

    def run(self):
        while self.queue.qsize():
            link = self.queue.get()
            url = link['api']+'q='+link['query']+'&n='+link['page_size']+'&page='+link['page_num']

            # proxy = random.choice(self.proxies)
            # proxies = {
            #             "http": proxy,
            #             "https": proxy,
            #         }
            try:
                wb_data = requests.get(url)
                if wb_data.content == '':
                    print('none')
                data = json.loads(wb_data.text)
                if data['itemsArray']:
                    for i in data['itemsArray']:
                        # self.db.update({'item_id': i["item_id"]}, {'$set': i}, True)
                        self.url_set.add(i["item_id"])
                else:
                    print(url,'found 0 items')
                # print(data['totalPage'])
                print(len(self.url_set))
                if link['page_num'] == '1':
                    # print(link['query'],data['totalPage'])
                    #
                    for i in range(2,int(data['totalPage'])+1):
                        temp_url = {
                            'api':link['api'],
                            'page_size':link['page_size'],
                            'page_num':str(i),
                            'query':link['query']
                        }
                        # print(temp_url)
                        self.queue.put(temp_url)

                    # pass
            except Exception as e:

                print(url,e)
            # except:
                self.queue.put(link)
                # if len(self.proxies) > 1:
                #     self.proxies.remove(proxy)
                #     # print()
                #     print('加载超时，重新写入Queue，代理{0}失效'.format(proxy))
                # else:
                #     self.proxies = GetAllIPs()
                #     print('加载超时，重新写入Queue，代理不足，重新获取')

            self.queue.task_done()


                # wb_data = requests.get(url, proxies=proxies, timeout=3)
            #     if wb_data.status_code == 200:
            #         data = json.loads(wb_data.text)
            #         if 'SUCCESS' in data['ret'][0]:
            #             data = json.loads(wb_data.text)
            #             # pass
            #             self.db.insert_one(data)
            #             print('爬取成功')
            #         else:
            #             if len(self.proxies) > 1:
            #                 self.proxies.remove(proxy)
            #                 print('代理{0}失效'.format(proxy))
            #             else:
            #                 self.proxies = GetAllIPs()
            #                 print('代理不足，重新获取')
            #                 # self.queue.put(url)
            #             self.queue.put(url)
            #             print('爬取失败，重新写入Queue')
            #     elif wb_data.status_code != 204:
            #         print('服务器错误')
            #         self.queue.put(url)
            #     else:
            #         print('状态码：{0}'.format(wb_data.status_code),url)
            # except:
            #     self.queue.put(url)
            #     if len(self.proxies) > 1:
            #         self.proxies.remove(proxy)
            #         # print()
            #         print('加载超时，重新写入Queue，代理{0}失效'.format(proxy))
            #     else:
            #         self.proxies = GetAllIPs()
            #         print('加载超时，重新写入Queue，代理不足，重新获取')
            #
            # self.queue.task_done()