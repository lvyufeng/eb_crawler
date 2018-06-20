
import os
import pickle
from urllib import parse
from utils.get_proxy import GetIP
def get_urls(file_path):
    urls = []
    with open(file_path,encoding='ISO-8859-1') as f:
        for line in f.readlines():
            split_line = line.split(',')
            if 'taobao' in split_line[0] or 'tmall' in split_line[0]:
                id = split_line[0].strip('\"').split('=')[-1]
                data = parse.quote('{"exParams":"{\"id\":\"'+id+'\"}","itemNumId":"'+id+'"}')
                urls.append('http://h5api.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0/?data=' + data)
            # print(urls)
            # print(split_line)
    f.close()
    return urls

def get_inner_id(file_path):
    ids = {}
    with open(file_path,encoding='ISO-8859-1') as f:
        for line in f.readlines():
            split_line = line.split(',')
            if 'taobao' in split_line[0] or 'tmall' in split_line[0]:
                id = split_line[0].strip('\"').split('=')[-1]
                # data = parse.quote('{"exParams":"{\"id\":\"'+id+'\"}","itemNumId":"'+id+'"}')
                # urls.append('http://h5api.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0/?data=' + data)
                try:
                    ids[id] = split_line[1].strip('\n').strip('"')
                except:
                    print(line)
            # print(urls)
            # print(split_line)
    f.close()
    return ids
import requests

# urls = get_urls('taskinfo.csv')
# # print(urls[0])
# url = urls[0]
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