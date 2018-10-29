import logging
from spider import config_parser,WebSpider,get_urls
import random
from utils import createInstance

def test_spider():
    """
    test spider
    """
    # initial config parser
    config = config_parser()
    # print(urls[-3304])
    # urls = urls[-3500:-1]
    keys = config.getStr('spider_config', 'platform').split(',')
    print(keys)
    for key in keys:
        print('Start %d spider %s' %(keys.index(key)+1,key))
        urls = get_urls(config,key)

        if key == 'Tmall':
            key = 'TaoBao'

        # initial fetcher / parser / saver
        fetcher = createInstance('crawlers',key+'SkuFetcher',max_repeat=1, sleep_time=0)
        parser = createInstance('crawlers',key+'SkuParser',max_deep=1)
        saver = createInstance('crawlers',key+'SkuSaver',config)
        if key == 'TaoBao':
            proxieser = createInstance('crawlers',key+'SkuProxieser',sleep_time=1)
        else:
            proxieser = None

    # initial web_spider
        web_spider = WebSpider(fetcher, parser, saver, proxieser, monitor_sleep_time=1)

    # add start url
        web_spider.set_start_url(urls)

    # start web_spider
        web_spider.start_working(fetcher_num=config.getInt('spider_config', 'threads'))

    # wait for finished
        web_spider.wait_for_finished()

    return

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s\t%(levelname)s\t%(message)s")
    test_spider()
    # test_spider_distributed()
    exit()