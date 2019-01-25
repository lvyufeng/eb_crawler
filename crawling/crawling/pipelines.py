# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo

class CrawlingPipeline(object):

    client = pymongo.MongoClient('202.202.5.140')
    db = client['test']
    # collection = db['temp_pdd']
    # sku_collection = db['temp_pdd_sku']

    def process_item(self, item, spider):
        try:
            self.db[item['collection']].insert(item._values)
        except Exception as e:
            print(e)



