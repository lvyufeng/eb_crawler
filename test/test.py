# from bs4 import BeautifulSoup
# import requests
# import re

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

# url = 'https://list.tmall.com/m/search_items.htm?page_size=20&page_no=2&q=%E9%87%8D%E5%BA%86%E8%B0%83%E5%91%B3'
#
# wb = requests.get(url)
# print(wb.text)
# list = re.compile(r"(?<=href=\"//).+?(?=\"class=\"sellPoint\")").findall(wb.text)
# next = re.compile(r"(?<=pagenum=\").+?(?=\")").findall(wb.text)
# pass

import pymysql

db = pymysql.connect("202.202.5.140", "root", "cqu1701", "eb")
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()


sql = 'SELECT b.three FROM threeclassificationtable a,threeclassificationtable b where a.two = b.two and a.three = %s'

db.close()