import time
import pymongo

client = pymongo.MongoClient('localhost',27017)
# client = pymongo.MongoClient('localhost',27017)
cars = client['test']
items = cars['url_test']

while True:
    print(items.count(),len(items.distinct('item_id')))
    # print(items.find().count())
    time.sleep(60)