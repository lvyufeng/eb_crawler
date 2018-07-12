import time
import pymongo

client = pymongo.MongoClient('localhost',27017)
# client = pymongo.MongoClient('localhost',27017)
cars = client['eb']
items = cars['taobao_06']

while True:
    print(items.count())
    # print(items.find().count())
    time.sleep(60)