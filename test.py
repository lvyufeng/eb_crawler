import re
import spider
import logging
import datetime
import requests
import json
from utils.import_url import get_urls
import time
import random

class SkuFetcher(spider.Fetcher):
    """
    fetcher module, only rewrite url_fetch()
    """
    def url_fetch(self, priority: int, url: str, keys: dict, deep: int, repeat: int, proxies=None):
        time.sleep(random.choice((1,2)))
        try:
            proxies = {
                "http": proxies,
                "https": proxies,
            }
            response = requests.get(url, proxies=proxies, timeout=5)

            if response.status_code == 200:
                data = json.loads(response.text)
                if 'SUCCESS' in data['ret'][0]:
                    # data = json.loads(response.text)
                    # pass
                    # self.db.insert_one(data)
                    # print('爬取成功')
                    content = (response.status_code, response.url, response.text)
                    return 1, True, content
                else:
                    # print('爬取失败，重新写入Queue')
                    return 0, False, None
            elif response.status_code != 204:
                # print('服务器错误')
                return 0, False, None
            else:
                # print('状态码：{0}'.format(response.status_code), url)

                return -1, False, None
        except:
            # print('加载超时，重新写入Queue')
            return 0, False, None


class SkuParser(spider.Parser):
    """
    parser module, only rewrite htm_parse()
    """
    def htm_parse(self, priority: int, url: str, keys: dict, deep: int, content: object):
        status_code, url_now, html_text = content

        url_list = []
        data = json.loads(html_text)
        save_list = [data] if data else []
        # print(save_list)

        return 1, url_list, save_list

class SkuSaver(spider.Saver):

    def item_save(self, url: str, keys: dict, item: (list, tuple)):
        """
        save the item of a url, you can rewrite this function, parameters and return refer to self.working()
        """
        self._save_pipe.write(str(item) + "\n\n")
        self._save_pipe.flush()
        return 1

class SkuProxieser(spider.Proxieser):

    def proxies_get(self):
        url = 'http://localhost:5010/get_all/'
        wb_data = requests.get(url)
        # print(wb_data.content)
        proxies = []
        for i in eval(wb_data.text):
            proxies.append(i)
        # print(len(proxies))
        return 0,proxies



def test_spider():
    """
    test spider
    """
    # initial fetcher / parser / saver
    fetcher = SkuFetcher(max_repeat=1, sleep_time=0)
    parser = SkuParser(max_deep=1)
    saver = SkuSaver(save_pipe=open("out_thread.txt", "w"))
    proxieser = SkuProxieser(sleep_time=1)

    # initial web_spider
    web_spider = spider.WebSpider(fetcher, parser, saver, proxieser, monitor_sleep_time=1)

    urls = get_urls('/home/lv/PycharmProject/eb_crawler/multi_threads/utils/taskinfo.csv','taobao')

    # add start url
    web_spider.set_start_url(urls)

    # start web_spider
    web_spider.start_working(fetcher_num=40)

    # wait for finished
    web_spider.wait_for_finished()
    return

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s\t%(levelname)s\t%(message)s")
    test_spider()
    # test_spider_distributed()
    exit()