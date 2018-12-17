import pymongo
import pymysql
import datetime
from decimal import Decimal
from cut_keyword import compare_name_keyword
sku_keys = ['itemid','storeid','platform','name','salecount','commentcount','platform_categoryid','origin','province','city','factoryAddress','keyword','price','createtime','status']
# mongodb

client = pymongo.MongoClient('202.202.5.140')
database = client['test']
collection = database['data_201810']

# client = pymongo.MongoClient('localhost')
# database = client['test']
# collection = database['data_201812']
# mysql
db = pymysql.connect("202.202.5.140", "root", "cqu1701", "eb")
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()


def suning_category(category):
    cats = ['喂养用品', '奶粉', '营养辅食', '食品保健/酒水饮料', '进口食品', '生鲜']
    if category in cats:
        return True
    else:
        return False

def pre_prosessing_price(price,promprice):
    if price is None or price == '' or '?' in price:
        price = '0'
    if promprice is None or promprice == '' or '?' in promprice:
        promprice = '0'

    if '-' in price and price.find('-') != 0:
        low = Decimal(price.split('-')[0])
        high = Decimal(price.split('-')[-1])

        price = ((high + low) / 2).quantize(Decimal('0.00'))
    else:
        try:
            price = Decimal(price).quantize(Decimal('0.00'))
        except:
            pass
    if '-' in promprice and promprice.find('-') != 0:
        low = Decimal(promprice.split('-')[0])
        high = Decimal(promprice.split('-')[-1])

        promprice = ((high + low) / 2).quantize(Decimal('0.00'))
    else:
        promprice = Decimal(promprice).quantize(Decimal('0.00'))

    if promprice > Decimal('0'):
        return promprice
    else:
        return price

    # pass

def find_area(city,data):
    data.pop('_id')
    try:
        data.pop['deliveryStartArea']
    except:
        pass
    keyword = data['keyword']
    data.pop('keyword')
    for i in data.values():
        try:
            if city in i:
                data['keyword'] = keyword
                return True
        except:
            continue

    return False

def find_store_location(city,data):
    try:
        if city in data['storeLocation']:
            # if 'storeLocation' in data else False
            return True
        else:
            return False
    except:
        return False
def get_store(data):
    store = {}

    store_kv = {'storeid':'storeActualID',
                'storename':'storeName',
                'company':'companyName',
                'province':'province',
                'city':'city',
                'platform' : 'website',
                'status': 1
                }

    if (data['website'] == 'Tmall' or data['website'] == 'TaoBao'):
        store_kv['company'] = 'factoryName'

    if data['website'] == 'JingDong':
        store_kv['province'] = 'storeLocation'

    for k,v in store_kv.items():
        try:
            store[k] = data[v]
        except:
            continue


    if data['website'] == 'TaoBao' and data['storeName'] == data['shopkeeper']:
        store['platform'] = 'Tmall'

    if data['website'] == 'SuNing':
        store['province'] = '重庆'
    if (data['website'] == 'Tmall' or data['website'] == 'TaoBao') and 'factoryAddress' in data:
        area = ['万州','涪陵','渝中','大渡口','江北','沙坪坝','九龙坡','南岸','北碚','綦江','大足','渝北','巴南','黔江','长寿','江津','合川','永川','南川','璧山','铜梁','潼南','荣昌','梁平','城口','丰都','垫江','武隆','忠县','开县','云阳','奉节','巫山','巫溪','石柱','秀山','酉阳','彭水',]

        for i in area:
            if i in data['factoryAddress']:
                store['city'] = i
                break

        # pass
        # if '区' in data['factoryAddress']:
        #     store['city'] = data['factoryAddress'][data['factoryAddress'].find('市')+1:data['factoryAddress'].find('区')+1]
        # elif '县' in data['factoryAddress']:
        #     store['city'] = data['factoryAddress'][data['factoryAddress'].find('市')+1:data['factoryAddress'].find('县')+1]



    store['status'] = 1
    return store


    pass

def get_sku(data):
    sku = {}


    sku_kv = {
                'itemid':'productActualID',
                'storeid':'storeActualID',
                'platform':'website',
                'name':'productName',
                'salecount':'monthSaleCount',
                'commentcount':'commentCount',
                'platform_categoryid':'categoryId',
                'origin':'origin',
                'province':'province',
                'city':'city',
                'factoryAddress':'factoryAddress',

                'keyword':'keyword',
    }

    if (data['website'] == 'Tmall' or data['website'] == 'TaoBao'):
        sku_kv['company'] = 'factoryName'

    if data['website'] == 'JingDong':
        sku_kv['province'] = 'storeLocation'


    for k,v in sku_kv.items():
        try:
            sku[k] = data[v]
        except:
            sku[k] = None
    if data['website'] == 'TaoBao' and data['storeName'] == data['shopkeeper']:
        sku['platform'] = 'Tmall'
    if sku['storeid'] == None:
        sku['storeid'] = '00000000'
    sku['price'] = pre_prosessing_price(data['productPrice'], data['productPromPrice'])
    sku['createtime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sku['status'] = 0




    if data['website'] == 'SuNing':
        sku['province'] = '重庆'
    if (data['website'] == 'Tmall' or data['website'] == 'TaoBao') and 'factoryAddress' in data:
        area = ['万州','涪陵','渝中','大渡口','江北','沙坪坝','九龙坡','南岸','北碚','綦江','大足','渝北','巴南','黔江','长寿','江津','合川','永川','南川','璧山','铜梁','潼南','荣昌','梁平','城口','丰都','垫江','武隆','忠县','开县','云阳','奉节','巫山','巫溪','石柱','秀山','酉阳','彭水',]

        for i in area:
            if i in data['factoryAddress']:
                sku['city'] = i
                break


    return sku

def trans_store():
    count = 0
    total = 0
    for i in collection.find():
        total = total + 1
        valid = find_area('重庆',i)
        if valid:
            if i['website'] == 'SuNing' and not suning_category(i['category1']):
                continue
            count = count + 1
            store = get_store(i)


            sql = 'insert into ' + 'store' + '(' + ','.join(store.keys()) + ') ' + 'values(' + ','.join(['%s' for i in store.keys()]) + ')'
            # print(store)
            # data = eval(i['website'])(i)
            # # + datetime.datetime.now().strftime('%Y%m')
            # sql = 'INSERT INTO ' + 'sku_201810' + '(' + ','.join(data.keys()) + ') ' + 'values(' + ','.join(['%s' for i in data.keys()]) + ')'
            try:
                # 执行sql语句
                cursor.execute(sql,tuple(store.values()))
                # 执行sql语句
                db.commit()
            except Exception as e:
                # 发生错误时回滚
                db.rollback()

        # count = count + 1
            print('total: %s, count: %s' %(total,count))
def trans_sku(table):
    sql = 'INSERT INTO ' + table + '(' + ','.join(sku_keys) + ') ' + 'values(' + ','.join(['%s' for i in sku_keys]) + ')'

    total = 0
    # sku_list = []
    for i in collection.find():
        total = total + 1
        valid = find_area('重庆',i)
        if valid:
            print(total)
            if i['website'] == 'SuNing' and not suning_category(i['category1']):
                continue
            sku = get_sku(i)
            matched = compare_name_keyword(sku['name'],sku['keyword'])
            if not matched:
                sku['keyword'] = '其他'
            # sku_list.append(tuple([sku[key] for key in sku_keys]))
            # pass
            # # + datetime.datetime.now().strftime('%Y%m')
            try:
            # 执行sql语句
                cursor.execute(sql, tuple([sku[key] for key in sku_keys]))
                # 执行sql语句
                db.commit()
            except Exception as e:
                # 发生错误时回滚
                db.rollback()
    # for i in sku_list:
    #     try:
    #         comment = int(i['commentcount'])
    #     except Exception as e:
    #         print(e)
    #         pass
    # try:
    #     # 执行sql语句
    #     cursor.executemany(sql, sku_list)
    #     # 执行sql语句
    #     db.commit()
    # except Exception as e:
    #     # 发生错误时回滚
    #     db.rollback()


# 关闭数据库连接
def find_city():
    # sql = 'INSERT INTO ' + 'sku_201810' + '(' + ','.join(sku_keys) + ') ' + 'values(' + ','.join(['%s' for i in sku_keys]) + ')'
    total = 0
    count = 0
    # sku_list = []
    for i in collection.find():
        total = total + 1
        valid = find_store_location('重庆',i)
        if valid:
            # sku = get_sku(i)
            count = count + 1
            print(total,count)

def find_category():
    # sql = 'INSERT INTO ' + 'sku_201810' + '(' + ','.join(sku_keys) + ') ' + 'values(' + ','.join(['%s' for i in sku_keys]) + ')'
    total = 0
    count = 0
    cat_list = []
    for i in collection.find():
        cat_list.append(i['category1'])

    print(set(cat_list))

# trans_sku('sku_201810')
# find_category()
# find_city()
trans_store()

db.close()
