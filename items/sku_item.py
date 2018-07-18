from .base_item import *

class SkuItem(DictItem):
    productActualID = Field()

    productCompleteID = Field()

    # 平台中自己的编号
    productURL = Field()
    # 链接
    productName = Field()
    # 商品名称
    productDescription = Field()
    # 描述信息
    shelveDate = Field()
    # 上架时间
    weight = Field()
    # 重量
    origin = Field()
    # 产地
    province = Field()
    # 所属省份
    city = Field()
    # 城市
    category = Field()
    # 类别
    specialtyCategory = Field()
    # 特产类别
    brand = Field()
    # 品牌
    factoryName = Field()
    # 生产厂商
    factoryAddress = Field()
    # 厂址
    series = Field()
    # 系列
    specification = Field()
    # 规格
    deliveryStartArea = Field()
    # 发货起始地址
    productPrice = Field()
    # 商品原始价格
    productPromPrice = Field()
    # 促销价格
    monthSaleCount = Field()
    # 月销量
    commentCount = Field()
    # 评论数量
    storeActualID = Field()
    # 平台中店铺的编号
    storeName = Field()
    # 店铺名称
    storeURL = Field()
    # 店铺链接
    shopkeeper = Field()
    # 掌柜、店家
    companyName = Field()
    # 公司名称
    storeLocation = Field()
    # 店铺所在地
    expirationDay = Field()
    # 商品过期日期
    produceDay = Field()
    # 生产日期
    productPromotionID = Field()
    # 商品促销编号，苏宁
    productCompleteID = Field()
    # 商品完整编号，苏宁
    category1 = Field()
    # 类别1
    category2 = Field()
    # 类别2
    category3 = Field()
    # 类别3
    goodCommentCount = Field()
    # 好评数量
    midCommentCount = Field()
    # 中评
    badCommentCount = Field()
    # 差评
    SaleCount = Field()
    # 总销量
    goodCommentRate = Field()
    # 好评率
    category4 = Field()
    # 类别4
    taxRate = Field()
    # 税率
    productHighVipPrice = Field()
    # 高级会员价格
    productLowVipPrice = Field()
    # 低级会员价格
    productTax = Field()
    # 税额
    pictureCommentCount = Field()
    # 带图评论
    additionCommentCount = Field()
    # 追评
    keyword = Field()
    # 关键词
    website = Field()
    # 网站
    extractTime = Field()
    # 提取时间
    analyzeTime = Field()
    # 分析时间，因为采集会跨月，在统计分析的时候需要将其统一在同一个月份
    errorInfo = Field()
    # 错误信息，如下架、移除、非农产品
    TaskDataID = Field()
    # 日志编号