from bs4 import BeautifulSoup
import requests
import re

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

url = 'http://search.suning.com/%E8%8B%B9%E6%9E%9C/'

wb = requests.get(url)
print(wb.text)
list = re.compile(r"(?<=href=\"//).+?(?=\"class=\"sellPoint\")").findall(wb.text)
next = re.compile(r"(?<=pagenum=\").+?(?=\")").findall(wb.text)
pass