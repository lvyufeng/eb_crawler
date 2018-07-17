import logging
from spider import config_parser,WebSpider,get_urls
# from crawlers import *

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
    for key in urls.keys():
        print(key)
        links = urls[key]
        if key == 'Tmall':
            key = 'Taobao'
        # initial fetcher / parser / saver
        fetcher = createInstance('crawlers',key+'SkuFetcher',max_repeat=1, sleep_time=0)
        parser = createInstance('crawlers',key+'SkuParser',max_deep=1)
        saver = createInstance('crawlers',key+'SkuSaver',config)
        proxieser = createInstance('crawlers',key+'SkuProxieser',sleep_time=1)
    # fetcher = SkuFetcher(max_repeat=1, sleep_time=0)
    # parser = SkuParser(max_deep=1)
    # saver = SkuSaver(config)
    # proxieser = SkuProxieser(sleep_time=1)

    # initial web_spider
        web_spider = WebSpider(fetcher, parser, saver, proxieser, monitor_sleep_time=1)


    # add start url
        web_spider.set_start_url(links)

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