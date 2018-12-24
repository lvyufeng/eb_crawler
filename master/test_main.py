import logging
from spider import config_parser,WebSpider
import random
from utils import createInstance,get_keywords


def test_spider():
    """
    test spider
    """
    # keys = ['YouLeGou','SuNing','Tmall','TaoBao','JingDong']
    config = config_parser('./../conf.ini')

    keys = ['TaoBao']
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

        keywords = ['重庆调味']
        # keywords = get_keywords()
        # urls = []
        for i in keywords:
            url = api.format(i)
            web_spider.set_start_url(url,keys={
                'website':key,
                'keyword':i,
                'params' : {
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
                    'data': '{{"q":"{0}","search":"提交","tab":"{2}","sst":"1","n":20,"buying":"buyitnow","m":"api4h5","token4h5":"","abtest":"29","wlsort":"29","page":{1}}}'.format(i, 1, 'all' if key == 'TaoBao' else 'mall')
                }
            })

        web_spiders.append(web_spider)


    for web_spider in web_spiders:
    # start web_spider
        web_spider.start_working(fetcher_num=1)
        print(web_spider.name)
        # wait for finished
        web_spider.wait_for_finished()

    return

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s\t%(levelname)s\t%(message)s")
    test_spider()
    # test_spider_distributed()
    exit()