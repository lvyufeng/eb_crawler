import requests
import json
import pymongo


client = pymongo.MongoClient('localhost',27017)
baidumap = client['baidumap']
result = baidumap['result']



url = 'http://api.map.baidu.com/place/v2/search?query=%E5%85%AC%E4%BA%A4%E7%AB%99&location=39.915,116.404&radius=1000&output=json&ak=c84xC1CLh6LmgivPbzzSqGvjUkuiAVAX'

wb = requests.get(url)

wb_data = json.loads(wb.text)

result.insert(wb_data)
pass