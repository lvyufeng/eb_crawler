import sys

try:
    from Queue import Queue  # py3
except:
    from queue import Queue  # py2

# sys.path.append('../')


from utils.config_parser import config_parser
from utils.get_urls import get_urls
import pymongo


class generalSpider():
    def __init__(self):
        self.queue = Queue()
        self.cf = config_parser()
        self.client = pymongo.MongoClient(self.cf.getStr('db', 'db_host'), self.cf.getInt('db', 'db_port'))
        # client = pymongo.MongoClient('localhost',27017)
        self.eb = self.client[self.cf.getStr('db', 'db_name')]

    def __crawl(self):
        """
        验证useful_proxy代理
        :param threads: 线程数
        :return:
        """
        if self.cf.getStr('spider_config','spider_type') == 'sku':
            from spiders.sku_spider import skuSpider as Spider
        else:
            from spiders.url_spider import urlSpider as Spider
            # spider = urlSpider(self.queue,self.eb,self.cf)

        thread_list = list()
        for index in range(self.cf.getInt('spider_config','threads')):
        # for index in range(20):
            thread_list.append(Spider(self.queue,self.eb,self.cf))

        for thread in thread_list:
            thread.daemon = True
            thread.start()
        # for thread in thread_list:
        #     thread.daemon = True
        #     thread.start()

        for thread in thread_list:
            thread.join()

    def main(self):
        self.putQueue()
        if not self.queue.empty():
            print("Start General Spider")
            self.__crawl()
        else:
            print('Crawl Complete!')


    def putQueue(self):
        """
        :param spider_type: 爬取类型：url或sku
        :return: None
        """
        # urls = get_urls(self.file_path,self.platform)

        if self.cf.getStr('spider_config','spider_type') == 'url':
            urls = get_urls(self.eb[self.cf.getStr('collections','keywords')],self.cf)
        else:
            urls = []
            # print('f')

        for url in urls:
            self.queue.put(url)

        # return urls


