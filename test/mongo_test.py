import pymongo

client = pymongo.MongoClient('localhost',27017)
db = client['test']
collection = db['product_info']

# collection.remove({'platform':'YouLeGou'})
# # print(collection.distinct('platform'))
print(collection.find({'platform':'SuNing'}).count())
# # lines = None
# with open('taskinfo.csv','r') as f:
#     lines = f.readlines()
#     print(len(lines))
#     for i in lines:
#         if 'ule' in i:
#             # print(i)
#             # pass
#             # if len(i.split(',')[-1].split('/')) == 5:
#             id = i.split(',')[-1].split('/')[-1].split('-')[0]
#             # print(id)
#             collection.insert_one({
#                 'sku_id':id,
#                 'platform':'YouLeGou'
#             })
# #
# f.close()
