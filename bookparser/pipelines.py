# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import scrapy
from pymongo import MongoClient


class BookparserPipeline:
    def __init__(self):
        self.client = MongoClient("localhost:27017")
        self.db = self.client["books"]

    def process_item(self, item, spider: scrapy.Spider):
        # print(item["url"], item["basic_price"], item["discount_price"], item["rating"])
        for _ in ["basic_price", "discount_price", "rating"]:
            try:
                if item[_]:
                    item[_] = item[_].replace(" р.", "")
                    item[_] = item[_].replace(" ", "")
                    item[_] = float(item[_])
            except Exception as e:
                print(item["url"])
                print(item[_])
                print(e)

        self.db[spider.name].update_one({'url': {"$eq": item['url']}}, {'$set': item}, upsert=True)
        return item
