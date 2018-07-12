import scrapy
# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

class TaobaoItem():



    def __init__(self):
        self.productActualID = ''

    # 平台中自己的编号
    productURL =
    # 链接
    productName =
    # 商品名称
    productDescription =
    # 描述信息
    shelveDate =
    # 上架时间
    weight =
    # 重量
    origin =
    # 产地
    province = scrapy.Field()
    # 所属省份
    city = scrapy.Field()
    # 城市
    category = scrapy.Field()
    # 类别
    specialtyCategory = scrapy.Field()
    # 特产类别
    brand = scrapy.Field()
    # 品牌
    factoryName = scrapy.Field()
    # 生产厂商
    factoryAddress = scrapy.Field()
    # 厂址
    series = scrapy.Field()
    # 系列
    specification = scrapy.Field()
    # 规格
    deliveryStartArea = scrapy.Field()
    # 发货起始地址
    productPrice = scrapy.Field()
    # 商品原始价格
    productPromPrice = scrapy.Field()
    # 促销价格
    monthSaleCount = scrapy.Field()
    # 月销量
    commentCount = scrapy.Field()
    # 评论数量
    storeActualID = scrapy.Field()
    # 平台中店铺的编号
    storeName = scrapy.Field()
    # 店铺名称
    storeURL = scrapy.Field()
    # 店铺链接
    shopkeeper = scrapy.Field()
    # 掌柜、店家
    companyName = scrapy.Field()
    # 公司名称
    storeLocation = scrapy.Field()
    # 店铺所在地
    expirationDay = scrapy.Field()
    # 商品过期日期
    produceDay = scrapy.Field()
    # 生产日期
    productPromotionID = scrapy.Field()
    # 商品促销编号，苏宁
    productCompleteID = scrapy.Field()
    # 商品完整编号，苏宁
    category1 = scrapy.Field()
    # 类别1
    category2 = scrapy.Field()
    # 类别2
    category3 = scrapy.Field()
    # 类别3
    goodCommentCount = scrapy.Field()
    # 好评数量
    midCommentCount = scrapy.Field()
    # 中评
    badCommentCount = scrapy.Field()
    # 差评
    SaleCount = scrapy.Field()
    # 总销量
    goodCommentRate = scrapy.Field()
    # 好评率
    category4 = scrapy.Field()
    # 类别4
    taxRate = scrapy.Field()
    # 税率
    productHighVipPrice = scrapy.Field()
    # 高级会员价格
    productLowVipPrice = scrapy.Field()
    # 低级会员价格
    productTax = scrapy.Field()
    # 税额
    pictureCommentCount = scrapy.Field()
    # 带图评论
    additionCommentCount = scrapy.Field()
    # 追评
    keyword = scrapy.Field()
    # 关键词
    website = scrapy.Field()
    # 网站
    extractTime = scrapy.Field()
    # 提取时间
    analyzeTime = scrapy.Field()
    # 分析时间，因为采集会跨月，在统计分析的时候需要将其统一在同一个月份
    errorInfo = scrapy.Field()
    # 错误信息，如下架、移除、非农产品
    TaskDataID = scrapy.Field()
    # 日志编号
    # pass