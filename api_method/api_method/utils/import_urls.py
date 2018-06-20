
import os
import pickle
from urllib import parse
from utils.get_proxy import GetIP
def get_urls(file_path):
    urls = []
    with open(file_path,encoding='ISO-8859-1') as f:
        for line in f.readlines():
            split_line = line.split(',')
            if 'taobao' in split_line[0]:
                id = split_line[0].strip('\"').split('=')[-1]
                data = parse.quote('{"exParams":"{\"id\":\"'+id+'\"}","itemNumId":"'+id+'"}')
                urls.append('http://h5api.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0/?data=' + data)
            # print(urls)
            # print(split_line)
    f.close()
    return urls

import requests

# urls = get_urls('taskinfo.csv')
# # print(urls[0])
# url = 'https://h5api.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0/?data=%7b%22exParams%22%3a%22%7b%22id%22%3a%22539334837731%22%7d%22%2c%22itemNumId%22%3a%22539334837731%22%7d'
# wb_data = requests.get(url)
# print(wb_data.text)
# for url in urls:
#     ip = GetIP()
#     print(ip,url)
#     proxies = {
#         "http": ip,
#         "https": ip,
#     }
#     try:
#         wb_data = requests.get(url,proxies=proxies,timeout=1)
#         print(wb_data.text)
#     except:
#         pass