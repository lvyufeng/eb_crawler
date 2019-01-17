import time
# import sched
# import apscheduler
import datetime
import schedule
import pymysql
import multiprocessing
from utils.mysql_connect import mysql_connect,select_all
from master.process import urlSpiderProcess
from spider import config_parser

# master主要完成事项：
# 1、从mysql获取任务
# 2、定时开始执行任务``
# 3、爬取url并添加到redis
# 4、爬取日志写入mysql


# 定时读取任务列表
def worker():
    db,cursor = mysql_connect('202.202.5.140','root','cqu1701','eb')
    all_task = select_all(cursor,'crawler_task')
    # task_process = []
    if all_task:
        for task in all_task:
            if condition_judgement(task):
                run_task(task,cursor)
    #             task_process.append(multiprocessing.Process(target = run_task, args = (task,)))
    # for process in task_process:
    #     process.start()
    db.close()

# 定时器
def scheduler():
    schedule.every(1).day.do(worker)
    # schedule.every().day.at('00:00').do(worker)

    while True:
        schedule.run_pending()
        time.sleep(1)

# 判断是否符合开始时间
def condition_judgement(task):
    today = datetime.datetime.strftime(datetime.datetime.now(),"%Y-%m-%d")
    condition_day = datetime.datetime.strftime(task[2],"%Y-%m-%d")
    if today == condition_day:
        return True
    else:
        return False

# 开始执行任务
def run_task(task,cursor):
    print('run task',datetime.datetime.today())
    config = config_parser('./../conf.ini')
    all_cralwer = select_all(cursor, 'crawler_task_crawler,crawler_crawler',{'crawler_task_crawler.task_id':str(task[0]),'crawler_task_crawler.crawler_id':'crawler_crawler.id'})
    task_process = []
    for i in all_cralwer:
        task_process.append(urlSpiderProcess(i[4],config))
    # task_process.append(urlSpiderProcess('Tmall', config))
    # task_process.append(urlSpiderProcess('TaoBao', config))

    for i in task_process:
        i.start()

# 完成任务，写入日志
def finish_task(task):
    pass

# main
if __name__ == "__main__":
    # scheduler()
    worker()
