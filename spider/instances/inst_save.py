# _*_ coding: utf-8 _*_

"""
inst_save.py by xianhu
"""

import sys
import logging
# import pymongo

class Saver(object):
    """
    class of Saver, must include function working()
    """

    def __init__(self, config):
        """
        constructor
        :param save_pipe: default sys.stdout, also can be a file handler
        """
        self.cf = config
        # self.client = pymongo.MongoClient(self.cf.getStr('db', 'db_host'), self.cf.getInt('db', 'db_port'))
        # # client = pymongo.MongoClient('localhost',27017)
        # self.eb = self.client[self.cf.getStr('db', 'db_name')]
        return

    def working(self, url: str, keys: dict, item: (list, tuple)) -> int:
        """
        working function, must "try, except" and don't change the parameters and return
        :return save_result: can be -1(save failed), 1(save success)
        """
        logging.debug("%s start: keys=%s, url=%s", self.__class__.__name__, keys, url)

        try:
            save_result = self.item_save(url, keys, item)
        except Exception as excep:
            save_result = -1
            logging.error("%s error: %s, keys=%s, url=%s", self.__class__.__name__, excep, keys, url)

        logging.debug("%s end: save_result=%s, url=%s", self.__class__.__name__, save_result, url)
        return save_result

    def item_save(self, url: str, keys: dict, item: (list, tuple)) -> int:
        """
        save the item of a url, you can rewrite this function, parameters and return refer to self.working()
        """

        return 1
