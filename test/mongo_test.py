import pymongo

client = pymongo.MongoClient('localhost',27017)
db = client['test']
collection = db['product_info']

# collection.remove({'platform':'SuNing'})
# print(collection.distinct('platform'))
print(collection.find_one({'platform':'SuNing'}))
# lines = None
# with open('taskinfo.csv','r') as f:
#     lines = f.readlines()
#     count = 0
#     for i in lines:
#         if 'product.suning' in i:
#             # print(i)
#             if len(i.split(',')[-1].split('/')) == 5:
#                 id = i.split(',')[-1].split('/')[-1].split('.')[0]
#                 shop_id = i.split(',')[-1].split('/')[-2]
#                 collection.insert_one({
#                     'sku_id':id,
#                     'shop_id':shop_id,
#                     'platform':'SuNing'
#                 })
#             else:
#                 count = count + 1
#     print(count)
#
# f.close()
