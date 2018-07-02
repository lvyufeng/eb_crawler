import pymongo
import json
from utils.import_urls import get_inner_id
import datetime
import pymysql

# 打开数据库连接
db = pymysql.connect("localhost", "root", "1701sky", "ebmis_db",use_unicode=True, charset="utf8")

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

# cursor.execute('select * from data_201805')
# keys = ','.join([i[0] for i in cursor.description])
# print(keys)
# 关闭数据库连接
def process_item(db,cursor,sql):

    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # 如果发生错误则回滚
        db.rollback()



client = pymongo.MongoClient('localhost', 27017)
        # client = pymongo.MongoClient('localhost',27017)
eb = client['eb']
mongo = eb['from_api']

print(mongo.count())
valid = 0
not_valid = 0
items = mongo.find()
ids = get_inner_id('utils/taskinfo.csv')

for item in items:

    # data = json.loads(item.data)
    if 'item' in item['data']:
        # print(item['data']['item']['itemId'])
        valid = valid + 1
        try:
            value = json.loads(item['data']['apiStack'][0]['value'])
            monthSaleCount = value['item']['sellCount']
            deliveryStartArea = value['delivery']['from']
        except:
            # print(item['data']['item']['itemId'])
            not_valid = not_valid + 1
            print(valid,not_valid)
            continue
        productInnerId = int(ids[item['data']['item']['itemId']])

        productActualID = item['data']['item']['itemId']
        # 平台中自己的编号
        productURL = 'https://h5.m.taobao.com/awp/core/detail.htm?id='+ item['data']['item']['itemId']
        # 链接
        productName = item['data']['item']['title']
        # 商品名称
        productDescription = item['data']['item']['subtitle'] if 'subtitle' in item['data']['item'] else None
        # 描述信息
        # shelveDate = None
        # 上架时间

        weight = None
        # 重量
        origin = None
        # 产地
        province = None
        # 所属省份
        city = None
        # 城市
        category = None
        # 类别
        specialtyCategory = None
        # 特产类别
        brand = None
        # 品牌
        factoryName = None
        # 生产厂商
        factoryAddress = None
        # 厂址
        series = None
        # 系列
        # specification = None
        # 规格
        if item['data']['props']:
            for i in item['data']['props']['groupProps'][0]['基本信息']:
                if '净含量' in list(i.keys()):
                    weight = i['净含量']
                if '产地' in list(i.keys()):
                    origin = i['产地']
                if '省份' in list(i.keys()):
                    province = i['省份']
                if '城市' in list(i.keys()):
                    city = i['城市']
                if '种类' in list(i.keys()):
                    category = i
                if '品类' in list(i.keys()):
                    specialtyCategory = i['品类']
                if '品牌' in list(i.keys()):
                    brand = i['品牌']
                if '厂名' in list(i.keys()):
                    factoryName = i['厂名']
                if '厂址' in list(i.keys()):
                    factoryAddress = i['厂址']
                if '系列' in list(i.keys()):
                    series = i['系列']

        # deliveryStartArea = value['delivery']['from'] #if 'from' in value['delivery'] else None
        # 发货起始地址

        if value['price']['extraPrices']:

            productPrice = value['price']['extraPrices'][0]['priceText']
            # 商品原始价格
            productPromPrice = value['price']['price']['priceText']
        else:
            productPrice = value['price']['price']['priceText']
            # 商品原始价格
            productPromPrice = None
        # 促销价格
        # monthSaleCount = value['item']['sellCount']# if 'sellCount' in value['item'] else None
        # 月销量
        commentCount = item['data']['item']['commentCount']
        # 评论数量
        storeActualID = item['data']['seller']['shopId']
        # 平台中店铺的编号
        # try:
        storeName = item['data']['seller']['shopName'] if 'shopName' in item['data']['seller'] else None
        # except:
        #     pass
        # 店铺名称
        storeURL = item['data']['seller']['taoShopUrl']
        # 店铺链接
        shopkeeper = item['data']['seller']['sellerNick']
        # 掌柜、店家
        # companyName = None
        # 公司名称
        # storeLocation = None
        # 店铺所在地
        # expirationDay = scrapy.Field()
        # # 商品过期日期
        # produceDay = scrapy.Field()
        # # 生产日期
        # productPromotionID = scrapy.Field()
        # # 商品促销编号，苏宁
        # productCompleteID = scrapy.Field()
        # # 商品完整编号，苏宁
        # category1 = scrapy.Field()
        # # 类别1
        # category2 = scrapy.Field()
        # # 类别2
        # category3 = scrapy.Field()
        # # 类别3
        # goodCommentCount = scrapy.Field()
        # # 好评数量
        # midCommentCount = scrapy.Field()
        # # 中评
        # badCommentCount = scrapy.Field()
        # # 差评
        # SaleCount = scrapy.Field()
        # # 总销量
        # goodCommentRate = scrapy.Field()
        # # 好评率
        # category4 = scrapy.Field()
        # # 类别4
        # taxRate = scrapy.Field()
        # # 税率
        # productHighVipPrice = scrapy.Field()
        # # 高级会员价格
        # productLowVipPrice = scrapy.Field()
        # # 低级会员价格
        # productTax = scrapy.Field()
        # # 税额
        # pictureCommentCount = scrapy.Field()
        # # 带图评论
        # additionCommentCount = scrapy.Field()
        # 追评
        keyword = None
        # 关键词
        website = 'TaoBao'
        # 网站
        extractTime = datetime.datetime.now().strftime("%Y-%m-%d")
        # 提取时间
        # analyzeTime = scrapy.Field()
        # # 分析时间，因为采集会跨月，在统计分析的时候需要将其统一在同一个月份
        errorInfo = value['trade']['hintBanner']['text'] if value['trade']['hintBanner'] else None
        # # 错误信息，如下架、移除、非农产品
        # TaskDataID = scrapy.Field()
        insert_sql = """
                        insert into data_201805(productInnerId,productActualID,productURL,productName,productDescription,weight,origin,province,city,category,specialtyCategory,brand,factoryName,factoryAddress,series,deliveryStartArea,productPrice,productPromPrice,monthSaleCount,commentCount,storeActualID,storeName,storeURL,shopkeeper,website,extractTime,errorInfo)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    """

        try:
            # 执行sql语句
            cursor.execute(insert_sql, (
            productInnerId, productActualID, productURL, productName, productDescription, weight, origin, province,
            city, category, specialtyCategory, brand, factoryName, factoryAddress, series, deliveryStartArea,
            productPrice, productPromPrice, monthSaleCount, commentCount, storeActualID, storeName, storeURL,
            shopkeeper, website, extractTime, errorInfo))
            # 提交到数据库执行
            db.commit()
        except:
            # 如果发生错误则回滚
            db.rollback()
        # print(item['data']['item']['itemId'])
    else:
        pass
        # print(item['data'])
db.close()

# print(valid)