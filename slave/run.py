import psutil
import schedule
import time
import sys
import redis

def main():
    redis_cli = redis.Redis.from_url("redis://202.202.5.140:6379", decode_responses=True)
    dbs = redis_cli.keys("sku*")  # 获得当前数据库所有的“key*”
    print(dbs)  # 查看key是否存在

def control_process():
    while True:
        text = input('input')
        print(text)


def scheduler():
    schedule.every(1).second.do(main)
    # schedule.every().day.at('00:00').do(worker)

    while True:
        schedule.run_pending()
        time.sleep(1)

def stop(pid):
    p = psutil.Process(pid)
    p.suspend()

def wake(pid):
    p = psutil.Process(pid)
    p.resume()


if __name__ == '__main__':
    main()
    # scheduler()