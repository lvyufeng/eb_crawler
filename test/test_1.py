import pymongo

client = pymongo.MongoClient('localhost',27017)
# client = pymongo.MongoClient('localhost',27017)
test = client['test']
pd = test['product_info']