# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from twisted.enterprise import adbapi
from pymongo import MongoClient
from scrapy.exceptions import DropItem
class SlavePipeline(object):
    def process_item(self, item, spider):
        return item


class MongoPipeline(object):
    # mongodb 数据库存储
    collection_name = 'items'

    # 数据库名称
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        # 从settings 获取 MONGO_URI，MONGO_DATABASE
        return cls(
            mongo_uri=crawler.settings.get('MONGODB_SERVER'),
            mongo_db=crawler.settings.get('MONGODB_DB', 'items')
        )

    def open_spider(self, spider):
        # 数据库打开配置
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        # 数据库关闭
        self.client.close()

    def process_item(self, item, spider):
        # 数据库储存
        if item == {}:
            raise DropItem("空数据，不写入数据库: %s" % item)
        if self.db[self.collection_name].find({'productActualID': item["productActualID"]}):
            raise DropItem("数据重复，不写入数据库: %s" % item)
        # 这里通过mongodb进行了一个去重的操作，每次更新插入数据之前都会进行查询，判断要插入的url_token是否已经存在，如果不存在再进行数据插入，否则放弃数据
        self.db[self.collection_name].update({'productActualID': item["productActualID"]}, {'$set': item}, True)

        # self.db[self.collection_name].insert_one(dict(item))
        return item
        # 切记 一定要返回item进行后续的pipelines 数据处理