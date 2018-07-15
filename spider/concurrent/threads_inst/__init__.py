# _*_ coding: utf-8 _*_

"""
define threads instances of url_fetch, htm_parse, item_save and proxies for thread_pool
"""

from .threads_inst_base import TPEnum
from .threads_inst_monitor import MonitorThread
from .threads_inst_fetch import FetchThread
from .threads_inst_parse import ParseThread
from .threads_inst_save import SaveThread
from .threads_inst_proxies import ProxiesThread
