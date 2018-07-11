import sys
from utils.import_urls import get_urls
import argparse

try:
    from Queue import Queue  # py3
except:
    from queue import Queue  # py2

sys.path.append('../')

from spiders.sku_spider import skuSpider
from spiders.url_spider import urlSpider

class generalSpider():
    def __init__(self):
        self.queue = Queue()

    def __crawl(self,spider_type,threads=20):
        """
        验证useful_proxy代理
        :param threads: 线程数
        :return:
        """
        if spider_type == 'sku':
            spider = skuSpider(self.queue)
        else:
            spider = urlSpider(self.queue)

        thread_list = list()
        for index in range(threads):
            thread_list.append(spider)

        for thread in thread_list:
            thread.daemon = True
            thread.start()

        for thread in thread_list:
            thread.join()

    def main(self,spider_type):
        self.putQueue(spider_type)
        if not self.queue.empty():
            print("Start General Spider")
            self.__crawl(spider_type)
        else:
            print('Crawl Complete!')


    def putQueue(self,spider_type):
        """
        :param spider_type: 爬取类型：url或sku
        :return: None
        """
        # urls = get_urls(self.file_path,self.platform)
        # for url in urls:
        #     self.queue.put(url)
        print(spider_type)


