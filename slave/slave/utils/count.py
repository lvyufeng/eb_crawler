import time
import pymongo

client = pymongo.MongoClient('139.224.112.239',27017)
# client = pymongo.MongoClient('localhost',27017)
cars = client['eb']
items = cars['items']

while True:
    print(items.count())
    # print(items.find().count())
    time.sleep(60)