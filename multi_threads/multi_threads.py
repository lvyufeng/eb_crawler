import sys
import time
from utils.import_urls import get_urls
from utils.get_proxy import GetIP,GetAllIPs
try:
    from Queue import Queue  # py3
except:
    from queue import Queue  # py2

sys.path.append('../')
from spider import Spider

class TaobaoSpider():
    def __init__(self):
        self.queue = Queue()

    def __crawl(self, threads=20):
        """
        验证useful_proxy代理
        :param threads: 线程数
        :return:
        """
        thread_list = list()
        for index in range(threads):
            thread_list.append(Spider(self.queue))

        for thread in thread_list:
            thread.daemon = True
            thread.start()

        for thread in thread_list:
            thread.join()

    def main(self):
        self.putQueue()
        if not self.queue.empty():
            print("Start Taobao Spider")
            self.__crawl()
        else:
            print('Crawl Complete!')


    def putQueue(self):
        urls = get_urls('utils/taskinfo.csv')
        for url in urls:
            self.queue.put(url)


if __name__ == '__main__':
    p = TaobaoSpider()
    p.main()