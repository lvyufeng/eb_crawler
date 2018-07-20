import time
import pymongo

client = pymongo.MongoClient('localhost',27017)
# client = pymongo.MongoClient('localhost',27017)
cars = client['test']
jd = cars['JingDong_7']
suning = cars['SuNing_7']
while True:
    print(jd.count(),suning.count())
    # print(items.find().count())
    time.sleep(60)