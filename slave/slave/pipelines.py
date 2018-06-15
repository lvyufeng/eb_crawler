# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from twisted.enterprise import adbapi
from pymongo import MongoClient

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
        self.db[self.collection_name].insert_one(dict(item))
        return item
        # 切记 一定要返回item进行后续的pipelines 数据处理