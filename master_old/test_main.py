import logging
from spider import WebSpider
import random
from utils import createInstance,get_keywords,JsonConf


def test_spider():
    """
    test spider
    """
    config = JsonConf.load('./../conf.json')


    keys = config['url_api'].keys()
    fetcher = createInstance('url_crawler', 'UrlFetcher', max_repeat=2, sleep_time=1)
    parser = createInstance('url_crawler', 'UrlParser', max_deep=1)
    saver = createInstance('url_crawler', 'UrlSaver',config)
        # if need_proxy == '1':
    proxieser = createInstance('url_crawler', 'UrlProxieser', sleep_time=1)
        # else:
        #     proxieser = None

        # initial web_spider
    web_spider = WebSpider(fetcher,parser,saver,proxieser, monitor_sleep_time=1)
    keywords = get_keywords()
        # urls = []
    for i in keywords:
        for key in keys:
            api = config['url_api'][key]
            url = api.format(i)
            web_spider.set_start_url(url,keys={'key':key,
                                               'replace':config['json_replace'][key],
                                               'depth':config['url_depth'][key],
                                               'need_proxy':config['need_proxy'][key]
                                               })
        # web_spider.start_working(fetcher_num=2)
        # # wait for finished
        # web_spider.wait_for_finished()



    web_spider.start_working(fetcher_num=10)
        # wait for finished
    web_spider.wait_for_finished()

    return


logging.basicConfig(level=logging.INFO, format="%(asctime)s\t%(levelname)s\t%(message)s")
test_spider()
    # test_spider_distributed()
exit()