import logging
from spider import config_parser,WebSpider
import random
from utils import createInstance,get_keywords

from multiprocessing import Process

class urlSpiderProcess(Process):
    def __init__(self,name,config):
        Process.__init__(self)
        self.name = name
        self.config = config

    def run(self):
        logging.basicConfig(level=logging.INFO, format="%(asctime)s\t%(levelname)s\t%(message)s")

        need_proxy = self.config.getStr('need_proxy', self.name)

        fetcher = createInstance('url_crawlers', self.name + 'UrlFetcher', max_repeat=2, sleep_time=1)
        parser = createInstance('url_crawlers', self.name + 'UrlParser', max_deep=1)
        saver = createInstance('url_crawlers', self.name + 'UrlSaver')
        if need_proxy == '1':
            proxieser = createInstance('url_crawlers', self.name + 'UrlProxieser', sleep_time=1)
        else:
            proxieser = None



        # initial web_spider
        web_spider = WebSpider(self.name, fetcher, parser, saver, proxieser, monitor_sleep_time=5)

        keywords = get_keywords()
        # urls = []
        api = self.config.getStr('url_api', self.name)
        for i in keywords:
            url = api.format(i)
            web_spider.set_start_url(url, keys={
                'website': self.name,
                'keyword': i,
                'params': {
                    'jsv': '2.3.16',
                    'appKey': '12574478',
                    't': None,
                    'sign': None,
                    'api': 'mtop.taobao.wsearch.h5search',
                    'v': '1.0',
                    'H5Request': 'true',
                    'ecode': '1',
                    'type': 'jsonp',
                    'dataType': 'jsonp',
                    'callback': 'mtopjsonp1',
                    'data': '{{"q":"{0}","search":"提交","tab":"{2}","sst":"1","n":20,"buying":"buyitnow","m":"api4h5","token4h5":"","abtest":"29","wlsort":"29","page":{1}}}'.format(i, 1, 'all' if self.name == 'TaoBao' else 'mall')}
            })
        web_spider.start_working(fetcher_num=2)
        # wait for finished
        web_spider.wait_for_finished()



