import requests
from bs4 import BeautifulSoup
import pymongo
import re


client = pymongo.MongoClient('localhost',27017)
superman_db = client['sku']
superman_good_url = superman_db['xmy_url']
header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/601.4.4 (KHTML, like Gecko) Version/9.0.3 Safari/601.4.4',
          'Upgrade-Insecure-Requests':'1',
          'Referer':'http://www.xmy365.com/index?show=1'

          }
url = 'http://www.xmy365.com/elastic/goods/countPage/1/0?mianLand=-1'
a=requests.post(url,'goodsName=&typeName=',headers=header)
num=int(a.text)
for i in range(1,num):
    url='http://www.xmy365.com/elastic/goods/list/%d/0?mianLand=-1'%i
    a = requests.get(url,headers=header)
    soup = BeautifulSoup(a.text, 'lxml')
    b=soup.select("body > a")
    for o in b:

        id=o.attrs.get('href')[6:][:-4]
        name = o.select('li > div.shop-name')[0].text
        price = o.select('li > div.shop-price > span.price')[0].text[2:]
        salecount = o.select(' li > div.item-last > span.saled > span')[0].text[:-1]
        commentcount = o.select(' li > div.item-last > span.fr > span')[0].text
        #body > a:nth-child(1) > li > div.shop-price > span.price
        superman_good_url.insert({
            'name': name,
            'price': price,
            'comment': commentcount,
            'salecount': salecount,
            'itemid': id,
            'platform': "WeiDian"
        })
        print(id)



