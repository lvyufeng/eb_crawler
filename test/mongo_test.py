import pymongo

client = pymongo.MongoClient('localhost',27017)
db = client['test']
collection = db['product_info']

# collection.remove({'platform':'YouLeGou'})
# # print(collection.distinct('platform'))
print(collection.find({'platform':'JingDong'}).count())
# # lines = None
# with open('taskinfo.csv','r') as f:
#     lines = f.readlines()
#     print(len(lines))
#     for i in lines:
#         if 'jd' in i:
#             id = i.split(',')[-1].split('/')[-1].split('.')[0]
#             inner_id = i.split(',')[0].strip('"')
#             # print(i,id,inner_id)
#             # if collection.find_one({'productActualID': id}):
#             item = {
#                 'sku_id': id,
#                 'inner_id':inner_id,
#                 'platform':'JingDong'
#             }
#             collection.insert_one(item)
#         elif  'suning' in i and len(i.split(',')[-1].split('/')) > 4:
#             id = i.split(',')[-1].split('/')[-1].split('.')[0]
#             shop_id = i.split(',')[-1].split('/')[-2]
#             inner_id = i.split(',')[0].strip('"')
#             # print(i, id, inner_id,shop_id)
#             # if collection.find_one({'productActualID': id}):
#             item = {
#                 'sku_id': id,
#                 'inner_id': inner_id,
#                 'shop_id':shop_id,
#                 'platform':'SuNing'
#             }
#             collection.insert_one(item)

# #
# f.close()
