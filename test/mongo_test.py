import pymongo

client = pymongo.MongoClient('localhost',27017)
db = client['test']
collection = db['product_info']

# collection.remove({'platform':'JingDong'})
# print(collection.distinct('platform'))
# print(collection.find_one({'platform':'JingDong'}))
# lines = None
with open('taskinfo.csv','r') as f:
    lines = f.readlines()
    for i in lines:
        if 'jd' in i:
            id = i.split(',')[-1].split('/')[-1].split('.')[0]
            collection.insert_one({
                'sku_id':id,
                'platform':'JingDong'
            })