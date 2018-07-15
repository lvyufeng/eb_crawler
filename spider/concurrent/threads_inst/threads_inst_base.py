# _*_ coding: utf-8 _*_

"""
threads_inst_base.py by xianhu
"""

import enum
import time
import queue
import logging
import threading


class TPEnum(enum.Enum):
    """
    enum of TPEnum, to mark the status of the web_spider
    """
    TASKS_RUNNING = "tasks_running"         # flag of tasks_running

    URL_FETCH = "url_fetch"                 # flag of url_fetch **
    URL_FETCH_NOT = "url_fetch_not"         # flag of url_fetch_not
    URL_FETCH_SUCC = "url_fetch_succ"       # flag of url_fetch_succ
    URL_FETCH_FAIL = "url_fetch_fail"       # flag of url_fetch_fail
    URL_FETCH_COUNT = "url_fetch_count"     # flag of url_fetch_count, for priority_queue

    HTM_PARSE = "htm_parse"                 # flag of htm_parse **
    HTM_PARSE_NOT = "htm_parse_not"         # flag of htm_parse_not
    HTM_PARSE_SUCC = "htm_parse_succ"       # flag of htm_parse_succ
    HTM_PARSE_FAIL = "htm_parse_fail"       # flag of htm_parse_fail

    ITEM_SAVE = "item_save"                 # flag of item_save **
    ITEM_SAVE_NOT = "item_save_not"         # flag of item_save_not
    ITEM_SAVE_SUCC = "item_save_succ"       # flag of item_save_succ
    ITEM_SAVE_FAIL = "item_save_fail"       # flag of item_save_fail

    PROXIES = "proxies"                     # flag of proxies **
    PROXIES_LEFT = "proxies_left"           # flag of proxies_left --> URL_FETCH_NOT
    PROXIES_FAIL = "proxies_fail"           # flag of proxies_fail --> URL_FETCH_FAIL


class BaseThread(threading.Thread):
    """
    class of BaseThread, as base class of each thread
    """

    def __init__(self, name, worker, pool):
        """
        constructor
        """
        threading.Thread.__init__(self, name=name)
        self._worker = worker
        self._pool = pool
        return

    def run(self):
        """
        rewrite run function, auto running and must call self.working()
        """
        logging.debug("%s[%s] start...", self.__class__.__name__, self.getName())

        while True:
            try:
                if not self.working():
                    break
            except (queue.Empty, TypeError):
                if self._pool.get_thread_stop_flag() and self._pool.is_all_tasks_done():
                    break
            except Exception as excep:
                logging.error("%s[%s] error: %s", self.__class__.__name__, self.getName(), excep)
                break

        logging.debug("%s[%s] end...", self.__class__.__name__, self.getName())
        return

    def working(self):
        """
        procedure of each thread, return True to continue, False to stop
        """
        raise NotImplementedError


