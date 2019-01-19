import requests
from urllib import parse
import json
import re

def get_single_keyword_info(list):
    pass

def get_ule(id,proxy,keyword):
    url = 'http://item.ule.com/item/{}-0-1.html'.format(id)
    proxies = {
        "http": proxy,
        "https": proxy,
    }
    # ua = UserAgent()
    # headers = {"User-Agent": ua.random}
    try:
        main_response = requests.get(url, proxies=proxies, timeout=3)  # ,headers = headers)
        if main_response.status_code != 200:
            return None
        # print(main_response.text)
        content = main_response.text
        item = {}

        item['website'] = ['YouLeGou']
        item['keyword'] = keyword
        item['productURL'] = [str(url)]

        item['productActualID'] = re.compile(r"(?<=listId = \').+?(?=\')").findall(content)
        item['productName'] = re.compile(r"(?<=listName = \').+?(?=\')").findall(content) + re.compile(
            r"(?<=<h1>).+?(?=<)").findall(content)
        item['brand'] = re.compile(r"(?<=brandName: ').+?(?=')").findall(content)
        item['factoryName'] = re.compile(r"(?<=merchantName = ').+?(?=')").findall(content)
        item['deliveryStartArea'] = re.compile(r"(?<=\"fArea\">)([\s\S]*?)(?=</span>)").findall(content)
        item['productPromPrice'] = re.compile(r"(?<=salePrice: ').+?(?=')").findall(content)
        item['productPrice'] = re.compile(r"(?<=maxPrice: ').+?(?=')").findall(content) + re.compile(
            r"(?<=salPrice=').+?(?=')").findall(content)
        item['weight'] = re.compile(r"(?<=weight =').+?(?=')").findall(content)
        item['commentCount'] = re.compile(r"(?<=商品评论\(<em>).+?(?=<)").findall(content)

        item['storeActualID'] = re.compile(r"(?<=storeId = ').+?(?=')").findall(content)
        item['storeName'] = re.compile(r"(?<=<a title=\").+?(?=\")").findall(content)
        # item['storeURL'] =
        item['companyName'] = item['factoryName']
        item['categoryId'] = re.compile(r"(?<=rootCateId: ').+?(?=')").findall(content)

        for k, v in item.items():
            item[k] = v[0].strip() if v else ''
        if item['deliveryStartArea'] != '':
            item['deliveryStartArea'] = str(item['deliveryStartArea']).replace('<span>', '').strip()

        if item['productActualID']:
            return item
        else:
            return None

    except Exception as e:
        # print(url,e)
        # print('加载超时，重新写入Queue')
        return None

def get_jd(id,proxy,keyword):
    pass

def get_suning(id,proxy,keyword):
    proxies = {
        "http": proxy,
        "https": proxy,
    }
    try:
        main_response = requests.get(url, proxies=proxies, timeout=3)
        if main_response.status_code == 218 or main_response.status_code == 404:
            return -1, False, None

        if main_response.status_code != 200:
            return 0, False, None
        # print(main_response.text)
        return 1, True, main_response.text
    except:
        pass

def get_taobao_tmall(id,proxy,keyword):
    url = 'http://h5api.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0/?data=' + parse.quote(
        '{"exParams":"{\"id\":\"' + id + '\"}","itemNumId":"' + id + '"}')
    try:
        proxies = {
            "http": proxy,
            "https": proxy,
        }

        response = requests.get(url, proxies=proxies, timeout=5)

        if response.status_code != 200:
            return None
        data = json.loads(response.text)
        if 'SUCCESS' not in data['ret'][0]:
            return None

        item = {}

        if 'item' in data['data']:
            try:
                value = json.loads(data['data']['apiStack'][0]['value'])
            except:
                return -1, [], []
            item['website'] = 'TaoBao' if data['data']['seller']['shopType'] == 'C' else 'Tmall'
            item['keyword'] = keyword
            item['productURL'] = url
            item['categoryId'] = data['data']['item']['rootCategoryId'] if 'itemId' in data['data'][
                    'item'] else None
                # 链接
            item['productActualID'] = data['data']['item']['itemId'] if 'itemId' in data['data']['item'] else None

            item['productName'] = data['data']['item']['title'] if 'title' in data['data']['item'] else None
                # 商品名称
            item['productDescription'] = data['data']['item']['subtitle'] if 'subtitle' in data['data'][
                    'item'] else None

            if data['data']['props']:
                for i in data['data']['props']['groupProps'][0]['基本信息']:
                    if '净含量' in list(i.keys()):
                        item['weight'] = i['净含量']
                    if '产地' in list(i.keys()):
                        item['origin'] = i['产地']
                    if '省份' in list(i.keys()):
                        item['province'] = i['省份']
                    if '城市' in list(i.keys()):
                        item['city'] = i['城市']
                    if '种类' in list(i.keys()):
                        item['category'] = i['种类']
                    if '品类' in list(i.keys()):
                        item['specialtyCategory'] = i['品类']
                    if '品牌' in list(i.keys()):
                        item['brand'] = i['品牌']
                    if '厂名' in list(i.keys()):
                        item['factoryName'] = i['厂名']
                    if '厂址' in list(i.keys()):
                        item['factoryAddress'] = i['厂址']
                    if '系列' in list(i.keys()):
                        item['series'] = i['系列']

            if 'extraPrices' in value['price']:
                item['productPrice'] = value['price']['extraPrices'][0]['priceText'] if value['price']['extraPrices'] else None

                item['productPromPrice'] = value['price']['price']['priceText']
            else:
                item['productPrice'] = value['price']['price']['priceText']
                    # 商品原始价格
                item['productPromPrice'] = None
                # 促销价格
            item['monthSaleCount'] = value['item']['sellCount'] if 'sellCount' in value['item'] else None
                # item['monthSaleCount'] = value['item']['sellCount']
            item['deliveryStartArea'] = value['delivery']['from'] if 'from' in value['delivery'] else None
                # 月销量
            item['commentCount'] = data['data']['item']['commentCount'] if 'commentCount' in data['data']['item'] else None
                # 评论数量
            item['storeActualID'] = data['data']['seller']['shopId'] if 'shopId' in data['data']['seller'] else None
                # 平台中店铺的编号
            item['storeName'] = data['data']['seller']['shopName'] if 'shopName' in data['data']['seller'] else None

                # 店铺名称
            item['storeURL'] = data['data']['seller']['taoShopUrl'] if 'taoShopUrl' in data['data']['seller'] else None

                # 店铺链接
            item['shopkeeper'] = data['data']['seller']['sellerNick'] if 'sellerNick' in data['data']['seller'] else None

                # item['errorInfo'] = value['trade']['hintBanner']['text'] if 'hintBanner' in value['trade'] else None
        else:
            return None

        # print(save_list)

        return item

    except:
        # print('加载超时，重新写入Queue')
        return None
