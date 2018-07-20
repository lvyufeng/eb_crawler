import pymongo
# import config_parser
from urllib import parse
import datetime

def get_urls(config):
    client = pymongo.MongoClient(config.getStr('db', 'db_host'), config.getInt('db', 'db_port'))
    # client = pymongo.MongoClient('localhost',27017)
    eb = client[config.getStr('db', 'db_name')]
    db = eb[config.getStr('db', 'product_info')]
    # store_db = eb[config.getStr('spider_config', 'platform') + '_' + str(datetime.datetime.now().month)]
    platform = config.getStr('spider_config', 'platform')
    # store_ids = [i['productActualID'] for i in store_db.find()]
    id_list = [i for i in db.find({'platform':platform})]
    # for i in id_list:
    #     if i['']
    url_list = generate_urls(id_list,platform)

    return url_list

def generate_urls(id_list,platform):

    url_list = {}
    if platform == 'TaoBao' or platform == 'Tmall':
        url_list[platform] = ['http://h5api.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0/?data=' + parse.quote('{"exParams":"{\"id\":\"' + i['sku_id'] + '\"}","itemNumId":"' + i['sku_id'] + '"}') for i in id_list]

    elif platform == 'JingDong':
        url_list[platform] = [
                'http://item.jd.com/%s.html'
                %(i['sku_id']) for i in id_list
        ]
    elif platform == 'SuNing':
        url_list[platform] = [
                'http://product.suning.com/%s/%s.html' % (i['shop_id'],
                i['sku_id']) for i in id_list
        ]

    return url_list
