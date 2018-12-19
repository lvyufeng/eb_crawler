import time
import logging
from .threads_inst_base import TPEnum, BaseThread


class MonitorThread(BaseThread):

    def __init__(self, name, pool, sleep_time=5):
        """
        constructor of MonitorThread
        """
        BaseThread.__init__(self, name, None, pool)

        self._sleep_time = sleep_time
        self._init_time = time.time()

        self._last_fetch_num = 0
        self._last_parse_num = 0
        self._last_save_num = 0
        return


    def working(self):
        """
        monitor the pool, auto running, and return False if you need stop thread
        """
        time.sleep(self._sleep_time)
        info = self.name + " running_tasks=%s;" % self._pool.get_number_dict(TPEnum.TASKS_RUNNING)

        cur_fetch_not = self._pool.get_number_dict(TPEnum.URL_FETCH_NOT)
        cur_fetch_succ = self._pool.get_number_dict(TPEnum.URL_FETCH_SUCC)
        cur_fetch_fail = self._pool.get_number_dict(TPEnum.URL_FETCH_FAIL)
        cur_fetch_all = cur_fetch_succ + cur_fetch_fail
        info += " fetch:[NOT=%d, SUCC=%d, FAIL=%d, %d/(%ds)];" % (cur_fetch_not, cur_fetch_succ, cur_fetch_fail, cur_fetch_all-self._last_fetch_num, self._sleep_time)
        self._last_fetch_num = cur_fetch_all

        cur_parse_not = self._pool.get_number_dict(TPEnum.HTM_PARSE_NOT)
        cur_parse_succ = self._pool.get_number_dict(TPEnum.HTM_PARSE_SUCC)
        cur_parse_fail = self._pool.get_number_dict(TPEnum.HTM_PARSE_FAIL)
        cur_parse_all = cur_parse_succ + cur_parse_fail
        info += " parse:[NOT=%d, SUCC=%d, FAIL=%d, %d/(%ds)];" % (cur_parse_not, cur_parse_succ, cur_parse_fail, cur_parse_all-self._last_parse_num, self._sleep_time)
        self._last_parse_num = cur_parse_all

        cur_save_not = self._pool.get_number_dict(TPEnum.ITEM_SAVE_NOT)
        cur_save_succ = self._pool.get_number_dict(TPEnum.ITEM_SAVE_SUCC)
        cur_save_fail = self._pool.get_number_dict(TPEnum.ITEM_SAVE_FAIL)
        cur_save_all = cur_save_succ + cur_save_fail
        info += " save:[NOT=%d, SUCC=%d, FAIL=%d, %d/(%ds)];" % (cur_save_not, cur_save_succ, cur_save_fail, cur_save_all-self._last_save_num, self._sleep_time)
        self._last_save_num = cur_save_all

        info += " proxies:[LEFT=%d, FAIL=%d];" % (self._pool.get_number_dict(TPEnum.PROXIES_LEFT), self._pool.get_number_dict(TPEnum.PROXIES_FAIL)) if self._pool.get_proxies_flag() else ""
        info += " total_seconds=%d" % (time.time() - self._init_time)

        logging.info(info)
        return not (self._pool.get_thread_stop_flag() and self._pool.is_all_tasks_done())


# MonitorThread = type("MonitorThread", (BaseThread, ), dict(__init__=init_monitor_thread, working=work_monitor))
