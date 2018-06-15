import time
import pymongo

client = pymongo.MongoClient('localhost',27017)
cars = client['eb']
items = cars['items']

while True:
    print(items.find().count())
    time.sleep(5)