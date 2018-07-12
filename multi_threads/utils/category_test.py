import pymongo
import pymysql

client = pymongo.MongoClient('localhost', 27017)
        # client = pymongo.MongoClient('localhost',27017)
eb = client['eb']
# mongo = eb['tmall']
mongo = eb['from_api']

items = mongo.find()
cate_ids = set([])
print(items.count())
for item in items:
    try:
        # print(item['data']['item']['categoryId'])
        cate_ids.add(item['data']['item']['categoryId'])
    except:
        # print(item)
        pass
print(len(cate_ids))
print(cate_ids)

db = pymysql.connect("localhost", "root", "19960704", "leimu",use_unicode=True, charset="utf8")
cursor = db.cursor()

def exe_select(category_id):
    print(category_id)
    sql = """SELECT `name` FROM y_category WHERE sid=%s"""
    cursor.execute(sql,category_id)
    # name = ''
    for r in cursor:
        print(r[0])
        # name = r[0]
        return r[0]
    # print(category_id, name)


for id in cate_ids:
    exe_select(id)