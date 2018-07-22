import pymongo

client = pymongo.MongoClient('localhost',27017)
# client = pymongo.MongoClient('localhost',27017)
test = client['test']
pd = test['test_tb']
print(pd.find().count())
#
# test = [1,2,3]
# t = (v for v in test)
# print(t,(1,2,3))