import logging
from spider import config_parser,WebSpider,get_urls
import random
from utils import createInstance,get_keywords

def test_spider():
    """
    test spider
    """
    # key = 'TaoBao'
    # key = 'JingDong'
    # keys = ['YouLeGou','SuNing','Tmall','TaoBao','JingDong']
    config = config_parser('./../conf.ini')
    keys = ['YouLeGou','SuNing','Tmall']
    web_spiders = []
    for key in keys:
        need_proxy = config.getStr('need_proxy', key)
        # initial fetcher / parser / saver
        fetcher = createInstance('url_crawlers', key + 'UrlFetcher', max_repeat=2, sleep_time=0)
        parser = createInstance('url_crawlers', key + 'UrlParser',max_deep=1)
        saver = createInstance('url_crawlers', key + 'UrlSaver')

        if need_proxy == '1':
            proxieser = createInstance('url_crawlers', key + 'UrlProxieser', sleep_time=1)
        else:
            proxieser = None

        # proxieser = None

        # initial web_spider
        web_spider = WebSpider(key,fetcher,parser,saver,proxieser, monitor_sleep_time=1)


        # initial config parser
        # config = config_parser('./../conf.ini')
        # print(urls[-3304])
        # urls = urls[-3500:-1]

        # api = config.getStr('url_api', 'taobao_url_api')
        api = config.getStr('url_api', key)

        keywords = get_keywords()
        # urls = []
        for i in keywords:
            url = api.format(i)
            web_spider.set_start_url(url,keys={
                'website':key,
                'keyword':i,
            })

        web_spiders.append(web_spider)


    for web_spider in web_spiders:
    # start web_spider
        web_spider.start_working(fetcher_num=10)
        print(web_spider.name)
        # wait for finished
        web_spider.wait_for_finished()

    return

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s\t%(levelname)s\t%(message)s")
    test_spider()
    # test_spider_distributed()
    exit()