import datetime
import pymongo
from spider import config_parser
import pymysql

config = config_parser('../conf.ini')


client = pymongo.MongoClient(config.getStr('db', 'db_host'),config.getInt('db', 'db_port'))
    # client = pymongo.MongoClient('localhost',27017)
eb = client[config.getStr('db', 'db_name')]
store_db = eb[config.getStr('spider_config', 'platform') + '_' + str(datetime.datetime.now().month)]

info_db = eb[config.getStr('db', 'product_info')]

db = pymysql.connect("localhost", "root", "19960704", "ebmis_db",use_unicode=True, charset="utf8")

# db = pymysql.connect("139.224.112.239", "root", "1701sky", "ebmis_db",use_unicode=True, charset="utf8")

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()


all = [i for i in store_db.find()]
inner_ids = {
    i['sku_id']:i['inner_id']
 for i in info_db.find()}

import re
fail = 0
count = 0
for i in all:
    i.pop('_id')
    # keys.remove()
    # print(i)
    try:
        for k,v in i.items():

            if isinstance(v,list):
                if k == 'brand':
                    i[k] = re.compile(r"(?<=>).+?(?=<)").findall(v[0]+'<')[0] if v else ''

                else:
                    i[k] = v[0].strip() if v else ''
        # i['brand'] = re.compile(r"(?<=>).*").findall(i['brand'][0])[0] if i['brand'] else ''
        # i['productName'] = i['productName'][0].strip() if i['productName'] and 'productName' in i else ''
        # i['weight'] = i['weight'][0] if i['weight'] and 'weight' in i else ''
        # i['origin'] = i['origin'][0] if i['origin'] and 'origin' in i else ''
        # i['category'] = i['category'][0] if i['category'] and 'category' in i else ''
        # i['specialtyCategory'] = i['specialtyCategory'][0] if i['specialtyCategory'] and 'specialtyCategory' in i else ''
        # i['specification'] = i['specification'][0] if i['specification'] and 'specification' in i else ''
    except Exception as e:
        fail = fail + 1
        continue
    try:
        i['productInnerId'] = inner_ids[str(i['productActualID'])]
    except:
        fail = fail + 1
        continue
    i['website'] = config.getStr('spider_config', 'platform')
    keys = list(i.keys())

    insert_sql = 'insert into data_201806_backup(' + ','.join(keys) + ') VALUES(' + ','.join(['%s' for key in keys]) + ')'
    # print(insert_sql)
    try:
        cursor.execute(insert_sql,tuple(str(i[key]) for key in keys))
    except:
        fail = fail + 1
        pass
    count = count + 1
    if count % 10000 == 0:
        db.commit()

    db.commit()
print(count,fail)
# 打开数据库连接


# cursor.execute('select * from data_201805')
# keys = ','.join([i[0] for i in cursor.description])
# print(keys)
# 关闭数据库连接
def process_item(db,cursor,datas):
    insert_sql = """insert into data_201805(productInnerId,productActualID,productURL,productName,productDescription,weight,origin,province,city,category,specialtyCategory,brand,factoryName,factoryAddress,series,deliveryStartArea,productPrice,productPromPrice,monthSaleCount,commentCount,storeActualID,storeName,storeURL,shopkeeper,website,extractTime,errorInfo)
                            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

    try:
        # 执行sql语句
        count = cursor.executemany(insert_sql,datas)
        # 提交到数据库执行
        print(count)
        db.commit()
        # time.sleep(60)
    except:
        # 如果发生错误则回滚
        db.rollback()

# print(mongo.count())
# valid = 0
# not_valid = 0
# items = mongo.find()
# ids = get_inner_id('utils/taskinfo.csv')
# datas = []
# for item in items:
#
#     # data = json.loads(item.data)
#     if 'item' in item['data']:
#         # print(item['data']['item']['itemId'])
#
#         try:
#             productInnerId = int(ids[item['data']['item']['itemId']])
#             value = json.loads(item['data']['apiStack'][0]['value'])
#             monthSaleCount = value['item']['sellCount']
#             deliveryStartArea = value['delivery']['from']
#         except:
#             # print(item['data']['item']['itemId'])
#             not_valid = not_valid + 1
#             # print(valid,not_valid)
#             continue
#         valid = valid + 1
#
#         productActualID = item['data']['item']['itemId']
#         # 平台中自己的编号
#         # productURL = 'https://h5.m.taobao.com/awp/core/detail.htm?id='+ item['data']['item']['itemId']
#         productURL = 'https://detail.tmall.com/item.htm?id='+ item['data']['item']['itemId']
#         # 链接
#         productName = item['data']['item']['title']
#         # 商品名称
#         productDescription = item['data']['item']['subtitle'] if 'subtitle' in item['data']['item'] else None
#         # 描述信息
#         # shelveDate = None
#         # 上架时间
#
#         weight = None
#         # 重量
#         origin = None
#         # 产地
#         province = None
#         # 所属省份
#         city = None
#         # 城市
#         category = None
#         # 类别
#         specialtyCategory = None
#         # 特产类别
#         brand = None
#         # 品牌
#         factoryName = None
#         # 生产厂商
#         factoryAddress = None
#         # 厂址
#         series = None
#         # 系列
#         # specification = None
#         # 规格
#         if item['data']['props']:
#             for i in item['data']['props']['groupProps'][0]['基本信息']:
#                 if '净含量' in list(i.keys()):
#                     weight = i['净含量']
#                 if '产地' in list(i.keys()):
#                     origin = i['产地']
#                 if '省份' in list(i.keys()):
#                     province = i['省份']
#                 if '城市' in list(i.keys()):
#                     city = i['城市']
#                 if '种类' in list(i.keys()):
#                     category = i['种类']
#                 if '品类' in list(i.keys()):
#                     specialtyCategory = i['品类']
#                 if '品牌' in list(i.keys()):
#                     brand = i['品牌']
#                 if '厂名' in list(i.keys()):
#                     factoryName = i['厂名']
#                 if '厂址' in list(i.keys()):
#                     factoryAddress = i['厂址']
#                 if '系列' in list(i.keys()):
#                     series = i['系列']
#
#         # deliveryStartArea = value['delivery']['from'] #if 'from' in value['delivery'] else None
#         # 发货起始地址
#
#         if 'extraPrices' in value['price']:
#
#             try:
#                 productPrice = value['price']['extraPrices'][0]['priceText'] if value['price']['extraPrices'] else None
#             except:
#                 print(productActualID)
#             # 商品原始价格
#             productPromPrice = value['price']['price']['priceText']
#         else:
#             productPrice = value['price']['price']['priceText']
#             # 商品原始价格
#             productPromPrice = None
#         # 促销价格
#         # monthSaleCount = value['item']['sellCount']# if 'sellCount' in value['item'] else None
#         # 月销量
#         commentCount = item['data']['item']['commentCount']
#         # 评论数量
#         storeActualID = item['data']['seller']['shopId']
#         # 平台中店铺的编号
#         # try:
#         storeName = item['data']['seller']['shopName'] if 'shopName' in item['data']['seller'] else None
#         # except:
#         #     pass
#         # 店铺名称
#         storeURL = item['data']['seller']['taoShopUrl']
#         # 店铺链接
#         shopkeeper = item['data']['seller']['sellerNick']
#         # 掌柜、店家
#         # companyName = None
#         # 公司名称
#         # storeLocation = None
#         # 店铺所在地
#         # expirationDay = scrapy.Field()
#         # # 商品过期日期
#         # produceDay = scrapy.Field()
#         # # 生产日期
#         # productPromotionID = scrapy.Field()
#         # # 商品促销编号，苏宁
#         # productCompleteID = scrapy.Field()
#         # # 商品完整编号，苏宁
#         # category1 = scrapy.Field()
#         # # 类别1
#         # category2 = scrapy.Field()
#         # # 类别2
#         # category3 = scrapy.Field()
#         # # 类别3
#         # goodCommentCount = scrapy.Field()
#         # # 好评数量
#         # midCommentCount = scrapy.Field()
#         # # 中评
#         # badCommentCount = scrapy.Field()
#         # # 差评
#         # SaleCount = scrapy.Field()
#         # # 总销量
#         # goodCommentRate = scrapy.Field()
#         # # 好评率
#         # category4 = scrapy.Field()
#         # # 类别4
#         # taxRate = scrapy.Field()
#         # # 税率
#         # productHighVipPrice = scrapy.Field()
#         # # 高级会员价格
#         # productLowVipPrice = scrapy.Field()
#         # # 低级会员价格
#         # productTax = scrapy.Field()
#         # # 税额
#         # pictureCommentCount = scrapy.Field()
#         # # 带图评论
#         # additionCommentCount = scrapy.Field()
#         # 追评
#         keyword = None
#         # 关键词
#         # website = 'TaoBao'
#         website = 'Tmall'
#
#         # 网站
#         extractTime = datetime.datetime.now().strftime("%Y-%m-%d")
#         # 提取时间
#         # analyzeTime = scrapy.Field()
#         # # 分析时间，因为采集会跨月，在统计分析的时候需要将其统一在同一个月份
#         try:
#             errorInfo = value['trade']['hintBanner']['text'] if 'hintBanner' in value['trade'] else None
#         except:
#             errorInfo = None
#         # # 错误信息，如下架、移除、非农产品
#         # TaskDataID = scrapy.Field()
#
#
#         data = (
#             productInnerId, productActualID, productURL, productName, productDescription, weight, origin, province,
#             city, category, specialtyCategory, brand, factoryName, factoryAddress, series, deliveryStartArea,
#             productPrice, productPromPrice, monthSaleCount, commentCount, storeActualID, storeName, storeURL,
#             shopkeeper, website, extractTime, errorInfo)
#
#         datas.append(data)
#         # print(item['data']['item']['itemId'])
#     else:
#         pass
#
#     if valid % 10000 == 0:
#         print(valid,len(datas))
#         process_item(db,cursor,datas)
#         datas = []
#         # print(item['data'])
# process_item(db,cursor,datas)
# db.close()

# print(valid)