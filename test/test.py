# _*_ coding: utf-8 _*_

"""
https://wq.jd.com/commodity/comment/getcommentlist?sku=11128347901
https://c0.3.cn/stock?skuId=11564571796&area=1_72_4137_0&venderId=186465&cat=12218,12221,13558&extraParam={%22originid%22:%221%22}
# url='https://item.m.jd.com/product/11128347901.html'
"""


import re
from bs4 import  BeautifulSoup
import requests
url = 'http://product.suning.com/136223634.html'
# url='http://item.jd.com/10000031268.html'
# url = 'https://chat1.jd.com/api/checkChat?pid=11564571796'

# test_url = 'http://c0.3.cn/stock?skuId=10000628007&area=1_72_4137_0&venderId={}&cat={}&extraParam={"originid":"1"}'
# print(test_url.format(1,2))

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    'Referer': 'https://item.m.jd.com/product/11564571796.html'

}
jd_data=requests.get(url,headers=headers)
print(jd_data.content)
# p1 = r"itemover"
p1 = r"(?<=sku-name\">\n).+?(?=<)"
test = '''
<div class="itemInfo-wrap">
                <div class="sku-name">
                                        艺福堂 袋泡茶 红枣姜茶 老姜茶茶 125g/盒*2                </div>
                        <div class="news">'''
pattern1 = re.compile(p1)#我们在编译这段正则表达式
matcher1 = pattern1.findall(test)#在源文本中搜索符合正则表达式的部分
print(matcher1)
#
# with open('test.html','w',encoding='gbk') as f:
#     f.write(jd_data.text)
# f.close()
# m = re.match(r'(?&lt;=skuid:\s{1,5})(\d{1,20})',jd_data.text)
soup=BeautifulSoup(jd_data.content,'lxml')
# import json
# print(json.loads(soup.select('script:nth-of-type(1)')[0].text.strip()))
productName=soup.select('div.sku-name')
print(productName)
# price=soup.select(' div span.price.J-p-1610639926')
# print(price)感觉需要调用API
weight =soup.select(' div.tab-con > div:nth-of-type(1) > div.p-parameter > ul.parameter2.p-parameter-list > li:nth-of-type(6)')
print(weight)
origin=soup.select(' div.tab-con > div:nth-of-type(2) > div.Ptable > div > dl > dd:nth-of-type(3) ')
print(origin)
category=soup.select('#detail > div.tab-con > div:nth-of-type(1) > div.p-parameter > ul.parameter2.p-parameter-list > li:nth-of-type(7)')
print(category)
brand=soup.select('div.tab-con > div:nth-of-type(1) > div.p-parameter > ul.parameter2.p-parameter-list > li:nth-of-type(1)')
print(brand)
commentCount=soup.select('#div.tab-main.large > ul > li.current')
print(commentCount)
companyname=soup.select(' div.tab-con > div:nth-of-type(1) > div.p-parameter > ul.parameter2.p-parameter-list > li:nth-of-type(3) > a')
print(companyname)
commentCount=soup.select('div.tab-main.small > ul > li:nth-of-type(4) ')
print(commentCount)
goodCommentCount=soup.select('div.mc > div.J-comments-list.comments-list.ETab > div.tab-main.small > ul > li:nth-of-type(5) > a > em ')
print(goodCommentCount)
# midCommentCount=soup.select(' div.mc > div.J-comments-list.comments-list.ETab > div.tab-main.small > ul > li:nth-of-type(5) > a > em')
# print(midCommentCount)
# badCommentCount=soup.select(' div.mc > div.J-comments-list.comments-list.ETab > div.tab-main.small > ul > li:nth-of-type(6) > a > em')
# print(badCommentCount)
productScore=soup.select(' div > div.mc > div > a > div.score-parts > div:nth-of-type(1) > span.score-detail > em')
print(productScore)
serviceAttitude=soup.select(' div > div.mc > div > a > div.score-parts > div:nth-of-type(2) > span.score-detail > em')
print(serviceAttitude)
logisticsSpeed=soup.select('div > div.mc > div > a > div.score-parts > div:nth-of-type(3) > span.score-detail > em')
print(logisticsSpeed)
