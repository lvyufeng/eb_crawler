from urllib import parse
from base import settings


def get_urls(file_path,platform):
    """
    :param file_path: 文件路径
    :param platform: 电商平台
    :return: url list
    """

    urls = []
    with open(file_path,encoding='ISO-8859-1') as f:
        for line in f.readlines():
            split_line = line.split(',')
            # 'taobao' in split_line[0] or 'tmall'
            if platform in split_line[0]:
                id = split_line[0].strip('\"').split('=')[-1]
                data = parse.quote('{"exParams":"{\"id\":\"'+id+'\"}","itemNumId":"'+id+'"}')
                urls.append(settings.taobao_sku_api + data)
            # print(urls)
            # print(split_line)
    f.close()
    return urls

def get_inner_id(file_path,platform):
    """

    :param file_path:
    :param platform:
    :return:
    """
    ids = {}
    with open(file_path,'r',encoding='ISO-8859-1') as f:
        for line in f.readlines():
            split_line = line.split(',')
            if platform in split_line[0]:
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


def get_keywords(file_path):
    """
    :param file_path:
    :return:
    """
    keywords = []
    with open(file_path,'r') as f:
        for line in f.readlines():
            keyword = line.strip('\n').strip('"')
            try:
                keywords.append(keyword)
            except:
                print(line)
            # print(urls)
            # print(split_line)
    f.close()
    return keywords

# keywords = get_keywords('keywords.csv')
# print(keywords)
# import requests
#
# urls = get_urls('taskinfo.csv')
# print(len(urls))
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