# _*_ coding: utf-8 _*_

"""
inst_fetch.py by xianhu
"""

import time
import random
import logging
import requests
from ..utilities import CONFIG_FETCH_MESSAGE


class Fetcher(object):
    """
    class of Fetcher, must include function working()
    """

    def __init__(self, max_repeat=3, sleep_time=0):
        """
        constructor
        :param max_repeat: default 3, maximum repeat count of fetching for a url
        :param sleep_time: default 0, sleeping time after a fetching for a url
        """
        self._max_repeat = max_repeat
        self._sleep_time = sleep_time
        return

    def working(self, priority: int, url: str, keys: dict, deep: int, repeat: int, proxies=None) -> (int, bool, object):
        """
        working function, must "try, except" and don't change the parameters and return
        :return fetch_result: can be -1(fetch failed), 0(need repeat), 1(fetch success)
        :return proxies_state: can be False(unavaiable), True(avaiable)
        :return content: can be any object, for example string, list, None, etc
        """
        logging.debug("%s start: %s", self.__class__.__name__, CONFIG_FETCH_MESSAGE % (priority, keys, deep, repeat, url))

        time.sleep(random.randint(0, self._sleep_time))
        try:
            fetch_result, proxies_state, content = self.url_fetch(priority, url, keys, deep, repeat, proxies=proxies)
        except Exception as excep:
            if repeat >= self._max_repeat:
                fetch_result, proxies_state, content = -1, False, None
                logging.error("%s error: %s, %s", self.__class__.__name__, excep, CONFIG_FETCH_MESSAGE % (priority, keys, deep, repeat, url))
            else:
                fetch_result, proxies_state, content = 0, False, None
                logging.debug("%s repeat: %s, %s", self.__class__.__name__, excep, CONFIG_FETCH_MESSAGE % (priority, keys, deep, repeat, url))

        logging.debug("%s end: fetch_result=%s, proxies_state=%s, url=%s", self.__class__.__name__, fetch_result, proxies_state, url)
        return fetch_result, proxies_state, content

    def url_fetch(self, priority: int, url: str, keys: dict, deep: int, repeat: int, proxies=None) -> (int, bool, object):
        """
        fetch the content of a url, you can rewrite this function, parameters and return refer to self.working()
        """
        response = requests.get(url, params=None, headers={}, data=None, proxies=proxies, timeout=(3.05, 10))
        if response.history:
            logging.debug("%s redirect: %s", self.__class__.__name__, CONFIG_FETCH_MESSAGE % (priority, keys, deep, repeat, url))

        content = (response.status_code, response.url, response.text)
        return 1, True, content
