import logging
from spider import config_parser,WebSpider,get_urls
import random
from utils import createInstance,get_keywords

def test_spider():
    """
    test spider
    """
    # key = 'TaoBao'
    key = 'JingDong'
    # initial fetcher / parser / saver
    fetcher = createInstance('url_crawlers', key + 'UrlFetcher', max_repeat=1, sleep_time=0)
    parser = createInstance('url_crawlers', key + 'UrlParser',max_deep=1)
    saver = createInstance('url_crawlers', key + 'UrlSaver')
    # proxieser = createInstance('crawlers',key+'SkuProxieser',sleep_time=1)

    # initial web_spider
    web_spider = WebSpider(fetcher,parser,saver, monitor_sleep_time=1)


    # initial config parser
    config = config_parser('./../conf.ini')
    # print(urls[-3304])
    # urls = urls[-3500:-1]

    # api = config.getStr('url_api', 'taobao_url_api')
    api = config.getStr('url_api', 'jd_url_api')

    keywords = get_keywords()
    # urls = []
    for i in keywords:
        url = api.format(i)
        web_spider.set_start_url(url,keys={
            'website':key,
            'keyword':i,
        })





    # add start url


    # start web_spider
    web_spider.start_working(fetcher_num=1)

    # wait for finished
    web_spider.wait_for_finished()

    return

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s\t%(levelname)s\t%(message)s")
    test_spider()
    # test_spider_distributed()
    exit()