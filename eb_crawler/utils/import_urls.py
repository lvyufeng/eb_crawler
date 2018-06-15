
import os
from eb_crawler.utils.redis_op import insert_data,redis_connect
from eb_crawler.utils.config_parse import config_parse

def get_urls(file_path):
    urls = []
    with open(file_path,encoding='ISO-8859-1') as f:
        for line in f.readlines():
            split_line = line.split(',')
            urls.append(split_line[0].strip('\"'))
            # print(urls)
            # print(split_line)
    f.close()
    return urls

def find_url_type(urls):
    config = config_parse('/Users/lvyufeng/PycharmProjects/eb_crawler/eb_crawler/configs/redis_config.ini')
    domins = {}
    host = config.get('redis','host')
    port = config.getint('redis','port')
    db = config.getint('redis','db')

    r = redis_connect(host,port,db)
    if r != None:
        for item in config.items('domin'):
            domins[item[-1]] = item[0]
        print(domins)
        for url in urls:
            for domin in domins.keys():
                if url.find(domin):

                    try:
                        type = config.get('url_type',domins[domin])
                        insert_data(r,type,url)
                    except Exception as e:
                        print(url)
                        print(e)
                        break
        print('import finished')
    else:
        print('can not connect redis')
urls = get_urls('/Users/lvyufeng/PycharmProjects/eb_crawler/eb_crawler/utils/taskinfo.csv')
find_url_type(urls)
