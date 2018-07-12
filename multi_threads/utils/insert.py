import pymongo
import sys

sys.path.append('../')
print(sys.path)
def insert_keywords():
    client = pymongo.MongoClient('localhost', 27017)
    eb = client['test']
    db = eb['keywords']
    datas = []
    with open('keywords.csv', 'r+') as f:
        for line in f.readlines():
            item = line.strip('\n').strip('"')
            data = {
                'keyword' : item
            }
            # print(data)
            datas.append(data)
    result = db.insert_many(datas)
    print(result.inserted_ids)

def insert_product_info():
    client = pymongo.MongoClient('localhost', 27017)
    eb = client['test']
    db = eb['product_info']
    datas = []
    ids = []
    with open('utils/product_baseinfo.csv','r+') as f:
        for line in f.readlines():
            item = line.split(',')
            data = {
                # 'innerid' : item[0].strip('"'),
                'sku_id' : item[1].strip('"'),
                'platform' : item[2].strip('\n').strip('"')
            }
            ids.append(item[1].strip('"'))
            # print(data)
            # if data not in datas:
            datas.append(data)

    result = db.insert_many(datas)
    print(len(result.inserted_ids))
    print(len(ids))
    print(len(set(ids)))
insert_keywords()
# insert_product_info()
