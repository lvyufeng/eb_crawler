from bs4 import BeautifulSoup
import requests


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
pass


data = []
with open('taobao_category.csv','r+') as f:
    for i in f.readlines():
        data.append(i.split(',')[0])

f.close()
data = set(data)
print(data)
pass