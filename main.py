import logging
from spider import config_parser,WebSpider,get_urls
import random


def createInstance(module_name, class_name, *args, **kwargs):
    module_meta = __import__(module_name, globals(), locals(), [class_name])
    class_meta = getattr(module_meta, class_name)
    obj = class_meta(*args, **kwargs)
    return obj

def test_spider():
    """
    test spider
    """
    # initial config parser
    config = config_parser()
    urls = get_urls(config)
    # print(urls[-3304])
    # urls = urls[-3500:-1]
    key = config.getStr('spider_config', 'platform')
    print(key)
    if key == 'Tmall':
        key = 'TaoBao'

    # links = urls[key]

    # initial fetcher / parser / saver
    fetcher = createInstance('crawlers',key+'SkuFetcher',max_repeat=1, sleep_time=0)
    # parser = None
    # saver = None

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