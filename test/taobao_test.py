import requests
import json
url = 'https://ai.taobao.com/search/getItem.htm?page={}&taobao=true&tmall=true&key=%E6%B6%AA%E9%99%B5%E6%A6%A8%E8%8F%9C&maxPageSize=200'

page = 1
taobao_items = []
tmall_items = []
while True:
    wb = requests.get(url.format(page))
    data = json.loads(wb.text)
    if not data['result']['auction']:
        break
    for i in data['result']['auction']:
        if i['userType'] == 1:
            tmall_items.append(i['itemId'])
        else:
            taobao_items.append(i['itemId'])
    page = page + 1

print('taobao:',len(taobao_items),len(set(taobao_items)))
print('tmall',len(tmall_items),len(set(tmall_items)))

