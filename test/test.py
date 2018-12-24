# from bs4 import BeautifulSoup
import requests
import re
import time
import json
import hashlib

# wb = requests.get('https://www.jd.com/allSort.aspx')
# soup = BeautifulSoup(wb.text,'lxml')
# list = soup.select('body > div:nth-of-type(5) > div.main-classify > div.list > div.category-items.clearfix > div > div > div.mc > div.items > dl > dd > a')
# data = {}
# for i in list:
#     data[i.text] = i.get('href').split('=')[-1]
#
# with open('jd_cat.csv','w+',encoding='gbk') as f:
#     for k,v in data.items():
#         f.write(k+','+v+'\n')
#
# f.close()
headers = {
    # 'accept-encoding': 'gzip, deflate, br',
    # 'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
    # 'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1',
    # 'accept': '*/*',
    # 'referer': 'https://h5.m.taobao.com/?sprefer=sypc00',
    # 'authority': 'h5api.m.taobao.com',
    # 'cookie': 't=cff5759b3198bafb639030a7296d6bff; cna=OOz3EwDBHU8CAS9eVNkZGaaY; thw=cn; _m_h5_tk=4dab06478749cf71bcb31296c169e46f_1534260967070; _m_h5_tk_enc=eb5abdfc8a3e52d0f7982d2ab34eb471; isg=BH9_A4W7GMQHLxzbVJKP32QcDlqleywDp44sWxFMGy51IJ-iGTRjVv02ZvbeeKt-',
}

params = {
    'jsv': '2.3.16',
    'appKey': '12574478',
    't': None,
    'sign': None,
    'api': 'mtop.taobao.wsearch.h5search',
    'v': '1.0',
    'H5Request': 'true',
    'ecode': '1',
    'type' : 'jsonp',
    'dataType': 'jsonp',
    'callback': 'mtopjsonp1',
    'data': '{"q":"重庆调味","search":"提交","tab":"all","sst":"1","n":20,"buying":"buyitnow","m":"api4h5","token4h5":"","abtest":"29","wlsort":"29","page":1}'
}

t = '{{"q":"{}","search":"提交","tab":"all","sst":"1","n":20,"buying":"buyitnow","m":"api4h5","token4h5":"","abtest":"29","wlsort":"29","page":{}}}'
t = t.format(1,2)
url = 'http://acs.m.taobao.com/h5/mtop.taobao.wsearch.h5search/1.0/'
#
wb = requests.get(url,params=params)

if '令牌为空' in wb.text:
    params['t'] = str(int(time.time()*1000))
    headers['cookie'] = '; '.join([i+'='+wb.cookies.get(i) for i in wb.cookies.keys()])
    src = wb.cookies.get('_m_h5_tk').split('_')[0]+'&'+params['t']+'&'+params['appKey']+'&'+params['data']
    m = hashlib.md5()
    m.update(src.encode('utf-8'))
    params['sign'] = m.hexdigest()
    tb = requests.get(url, params=params,headers=headers)
    data = json.loads(tb.text.replace('mtopjsonp1(','').replace(')',''))
pass



# url = 'https://list.tmall.com/m/search_items.htm'
# params = {
#     'page_size': 20,
#     'page_no': 6,
#     'q': '重庆调味',
#     'type': 'p',
#     'tmhkh5':'' ,
#     'spm': 'a220m.8599659.a2227oh.d100',
#     'from': 'mallfp..m_1_searchbutton'
# }
# wb = requests.get(url,params=params)
# print(wb.text)
# list = re.compile(r"(?<=href=\"//).+?(?=\"class=\"sellPoint\")").findall(wb.text)
# next = re.compile(r"(?<=pagenum=\").+?(?=\")").findall(wb.text)
# pass

# import pymysql
#
# db = pymysql.connect("202.202.5.140", "root", "cqu1701", "eb")
# # 使用 cursor() 方法创建一个游标对象 cursor
# cursor = db.cursor()
#
#
# sql = 'SELECT b.three FROM threeclassificationtable a,threeclassificationtable b where a.two = b.two and a.three = %s'
#
# db.close()