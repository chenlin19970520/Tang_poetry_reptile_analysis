# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.conf import settings
class TangPoetryPipeline(object):
    def __init__(self):
        host = settings["MONGODB_HOST"]
        port = settings["MONGODB_PORT"]
        #连接数据库
        client = pymongo.MongoClient(host = host,port = port)
        mydb = client['test']
        self.post = mydb['t']
    def process_item(self, item, spider):
        data = dict(item)
        self.post.insert(data)
# class QQNewMongoPipeline(object):
#     collection = 'tang
#     def __init__(self,mongo_uri,mongo_db):
#         self.mongo_uri = mongo_uri
#         self.mongo_db = mongo_db
#     @classmethod
#     def from_crawler(cls,crawler):
#         ...
#             scrapy 为我们提供了一个访问settings.py的方法，这里可以从
#             settings.py文件中获取数据库的url和名称
#         ...
#         return cls(
#             mongo_uri = crawler.settings.get('MONGO_URI')
#             mongo_db = crawler.settings.get('MONGO_DB')
#         )
#     def open_spider(self,spider):
#         #爬虫一旦打开就会实现这个方法，连接到数据库
#         self.client = pymongo.MongoClient(self,mongo_uri)
#         self.db = self.client[self.mongo_db]
#     def close_spider(self,spider):
#         self.client.close()

#     def process_item(self,item,spider):
#         if not item['title']:
#             return item
#         data={
            
#         }