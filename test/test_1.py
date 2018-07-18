from pymongo import MongoClient
import pprint

#连接到数据库
conn = MongoClient(host="127.0.0.1", port=27017)    #connect to mongodb
db = conn.test

#查一个collection
# print(db.test_collection)
print("test_collection")
array = db.test_collection.find()
for doc in array:
    print(doc)

#增加一个document
insert_doc = {"name":"test2", "age":30}
db.test_collection.insert(insert_doc)
# print(db.test_collection)
print("after inserting:")
array = list(db.test_collection.find())
pprint.pprint(array)


#修改记录
db.collection.update({"name":"test"},{"$set":{"age":33}})
# print(db.test_collection)
print("after updating:")
array = list(db.test_collection.find())
pprint.pprint(array)

# #删除一个collection中的所有数据
# db.test_collection.remove({})
# # print(db.test_collection)
# print("after deleting:")
# array = list(db.test_collection.find())
# pprint.pprint(array)