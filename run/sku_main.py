import logging
from spider import config_parser,WebSpider,get_urls
import random
from utils import createInstance
import pymongo


def test_spider():
    """
    test spider
    """
    client = pymongo.MongoClient('localhost')
    db = client['sku']
    collection = db['sku_ids']


    # initial config parser
    config = config_parser('./../conf.ini')
    # print(urls[-3304])
    # urls = urls[-3500:-1]
    keys = config.getStr('spider_config', 'platform').split(',')
    print(keys)
    for key in keys:
        print('Start %d spider %s' %(keys.index(key)+1,key))
        # urls = get_urls(config,key)
        need_proxy = config.getStr('need_proxy', key)
        # initial fetcher / parser / saver
        fetcher = createInstance('crawlers',key+'SkuFetcher',max_repeat=1, sleep_time=0)
        parser = createInstance('crawlers',key+'SkuParser',max_deep=1)
        saver = createInstance('crawlers',key+'SkuSaver',config)
        if need_proxy == '1':
            proxieser = createInstance('crawlers',key+'SkuProxieser',sleep_time=1)
        else:
            proxieser = None


    # initial web_spider
        web_spider = WebSpider(key,fetcher, parser, saver, proxieser, monitor_sleep_time=1)
        api = config.getStr('sku_api', key)
    # add start url
        for i in collection.find({'website':key}):
            url = api.format(i['_id'][1:])
            web_spider.set_start_url(url, keys={
                'website': key,
                'keyword': i['keyword'],
            })


    # start web_spider
        web_spider.start_working(fetcher_num=20)

    # wait for finished
        web_spider.wait_for_finished()

    return

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s\t%(levelname)s\t%(message)s")
    test_spider()
    # test_spider_distributed()
    exit()