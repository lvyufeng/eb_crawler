import time
# import sched
# import apscheduler
# import datetime
import schedule

# master主要完成事项：
# 1、从mysql获取任务
# 2、定时开始执行任务``
# 3、爬取url并添加到redis
# 4、爬取日志写入mysql


# 定时读取任务列表
def worker():
    print('test working')

schedule.every(1).minute.do(worker)
schedule.every().day.at('00:00').do(worker)

while True:
    schedule.run_pending()
    time.sleep(1)

# 判断是否符合开始时间


# 开始执行任务


# 完成任务，写入日志