import pymongo
# import config_parser
from urllib import parse

def get_urls(config):
    client = pymongo.MongoClient(config.getStr('db', 'db_host'), config.getInt('db', 'db_port'))
    # client = pymongo.MongoClient('localhost',27017)
    eb = client[config.getStr('db', 'db_name')]
    db = eb[config.getStr('db', 'product_info')]
    platforms = db.distinct('platform')
    print(platforms)
    id_list = {}
    for platform in platforms:
        id_list[platform] = [i for i in db.find({'platform':platform})]
        # id_list.append(ids)

    url_list = generate_urls(id_list,platforms)
    # url_list = ['http://h5api.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0/?data=' + parse.quote('{"exParams":"{\"id\":\"' + i['sku_id'] + '\"}","itemNumId":"' + i['sku_id'] + '"}') for i in db.find({'platform':'TaoBao'})]
    # pass

    return url_list

# """
# https://wq.jd.com/commodity/comment/getcommentlist?sku=11128347901
# https://c0.3.cn/stock?skuId=11564571796&area=1_72_4137_0&venderId=186465&cat=12218,12221,13558&extraParam={%22originid%22:%221%22}
# # url='https://item.m.jd.com/product/11128347901.html'
# """
def generate_urls(id_list,platforms):
    url_list = {}
    for platform in platforms:
        if platform == 'TaoBao' or platform == 'Tmall':
            pass
            # url_list[platform] = ['http://h5api.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0/?data=' + parse.quote('{"exParams":"{\"id\":\"' + i['sku_id'] + '\"}","itemNumId":"' + i['sku_id'] + '"}') for i in id_list[platform]]
        elif platform == 'JingDong':
            pass
            url_list[platform] = [
                'http://item.jd.com/%s.html'
                %(i['sku_id']) for i in id_list[platform]
            ]
        elif platform == 'SuNing':
            # url_list[platform] = [
            #     'http://product.suning.com/%s/%s.html,'
            #     'https://shop.suning.com/jsonp/{}/shopinfo/shopinfo.html,' \
            #     'https://pas.suning.com/nspcsale_0_{}_{}_{}_320_023_0230101_500353_1000333_9325_12583_Z001___R9006371.html' % (i['shop_id'],
            #     i['sku_id']) for i in id_list[platform]
            # ]
            pass


    return url_list
# get_urls(config_parser())
