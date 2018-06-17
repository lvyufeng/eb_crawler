import time
import pymongo

client = pymongo.MongoClient('139.224.112.239',27017)
cars = client['eb']
items = cars['items']

while True:
    print(len(items.distinct('productName')))
    # print(items.find().count())
    time.sleep(60)