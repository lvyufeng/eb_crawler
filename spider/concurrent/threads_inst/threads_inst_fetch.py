# _*_ coding: utf-8 _*_

"""
threads_inst_fetch.py by xianhu
"""

import time
import logging
from .threads_inst_base import TPEnum, BaseThread


class FetchThread(BaseThread):
    """
    class of FetchThread, as the subclass of BaseThread
    """

    def __init__(self, name, worker, pool):
        """
        constructor
        """
        BaseThread.__init__(self, name, worker, pool)
        self._proxies = None
        # self._proxies_order = 0
        return

    def working(self):
        """
        procedure of fetching, auto running, and return True
        """
        # ----*----
        if self._pool.get_proxies_flag() and (not self._proxies):
            self._proxies = self._pool.get_a_task(TPEnum.PROXIES)

            # self._proxies_order = temp[0]
        # print(self._proxies_order)
        # ----1----
        priority, counter, url, keys, deep, repeat = self._pool.get_a_task(TPEnum.URL_FETCH)

        # ----2----
        fetch_result, proxies_state, content = self._worker.working(priority, url, keys, deep, repeat, proxies=self._proxies)

        # ----3----
        if fetch_result > 0:
            self._pool.update_number_dict(TPEnum.URL_FETCH_SUCC, +1)
            if content is not None:
                self._pool.add_a_task(TPEnum.HTM_PARSE, (priority, counter, url, keys, deep, content))
            if content is not None and proxies_state == 1:
                self._pool.add_a_task(TPEnum.PROXIES,self._proxies)
        elif fetch_result == 0:
            self._pool.add_a_task(TPEnum.URL_FETCH, (priority, counter, url, keys, deep, repeat+1))
        else:
            self._pool.update_number_dict(TPEnum.URL_FETCH_FAIL, +1)

        # ----*----
        if self._proxies and proxies_state == -1:
            self._pool.update_number_dict(TPEnum.PROXIES_FAIL, +1)
            self._pool.finish_a_task(TPEnum.PROXIES)
            self._proxies = None
        # else:
        #     self._pool.add_a_task(TPEnum.PROXIES,self._proxies)

        # ----4----
        self._pool.finish_a_task(TPEnum.URL_FETCH)

        # ----*----
        while (self._pool.get_number_dict(TPEnum.HTM_PARSE_NOT) > 500) or (self._pool.get_number_dict(TPEnum.ITEM_SAVE_NOT) > 500):
            logging.debug("%s[%s] sleep 5 seconds because of too many 'HTM_PARSE_NOT' or 'ITEM_SAVE_NOT'...", self.__class__.__name__, self.getName())
            time.sleep(10)

        # ----5----
        # del fetch_result, proxies_state, content
        return True
