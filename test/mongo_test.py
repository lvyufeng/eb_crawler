import pymongo

client = pymongo.MongoClient('localhost',27017)
db = client['test']
collection = db['product_info_copy']

# collection.remove({'platform':'YouLeGou'})
# # print(collection.distinct('platform'))
# print(collection.find({'platform':'TaoBao'}).count())
# print(collection.find_one({'platform':'TaoBao'}))
# # lines = None
import pymysql
from spider import config_parser
config = config_parser('/Users/lvyufeng/PycharmProjects/eb_crawler/conf.ini')
db = pymysql.connect(config.getStr('mysql', 'host'), config.getStr('mysql', 'user'), config.getStr('mysql', 'passwd'), config.getStr('mysql', 'db'), use_unicode=True, charset="utf8")

cursor = db.cursor()
count = 0

with open('/Users/lvyufeng/PycharmProjects/eb_crawler/utils/taskinfo_1.csv','r',encoding='ISO-8859-15') as f:
    lines = f.readlines()
    print(len(lines))
    for i in lines:
        if 'taobao' in i:
            innerid = i.split(',')[-1].strip('\n').strip('"')
            url = i.split(',')[0].strip('"')
            website = 'TaoBao'
            status = 0
            # print(innerid,url)
            insert_sql = 'insert into taskinfo(Status,URL,Website,productInnerId) VALUES(%s,%s,%s,%s)'
            try:
                cursor.execute(insert_sql,(status,url,website,innerid))
                count = count + 1
            except:
                pass
    db.commit()
f.close()
print(count)
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
