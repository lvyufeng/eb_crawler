import requests
import json

# 202.202.5.140
def GetIP():
    url = 'http://localhost:5010/get/'
    wb_data = requests.get(url)
    if wb_data.text != 'no proxy!':
        return 'http://'+wb_data.text
    else:
        # print(wb_data.text)
        return None
    # print('http://'+wb_data.text)
def GetAllIPs():
    url = 'http://localhost:5010/get_all/'
    wb_data = requests.get(url)
    print(wb_data.content)
    proxies = []
    for i in eval(wb_data.text):
        proxies.append(i)
    # print(len(proxies))
    return proxies
    # tmp =list(eval(wb_data.content))
    # for i in tmp:
    #     print(tmp)
    # if wb_data.text != []:
    #     return 'http://' + wb_data.text
    # else:
    #     # print(wb_data.text)
    #     return wb_data.text
# GetAllIPs()
def DeleteIP(ip):
    url = 'http://202.202.5.140:5010/delete?proxy=' + ip
    res = requests.get(url)
    print(res.text)

# DeleteIP('114.115.182.59:3128')