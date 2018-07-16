import re
import spider
import logging
import datetime
import requests
import json

class SkuFetcher(spider.Fetcher):
    """
    fetcher module, only rewrite url_fetch()
    """
    def url_fetch(self, priority: int, url: str, keys: dict, deep: int, repeat: int, proxies=None):
        try:
            response = requests.get(url, proxies=proxies, timeout=3)
            if response.status_code == 200:
                data = json.loads(response.text)
                if 'SUCCESS' in data['ret'][0]:
                    # data = json.loads(response.text)
                    # pass
                    # self.db.insert_one(data)
                    print('爬取成功')
                    content = (response.status_code, response.url, response.text)
                    return 1, True, content
                else:
                    print('爬取失败，重新写入Queue')
                    return 0, False, None
            elif response.status_code != 204:
                print('服务器错误')
                return 0, False, None
            else:
                print('状态码：{0}'.format(response.status_code), url)
        except:
            return -1, False, None
