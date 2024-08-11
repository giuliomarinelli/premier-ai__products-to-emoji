# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo


class GetSupermarketProductsDataPipeline:
    def process_item(self, item, spider):
        return item

# get_data_project/pipelines.py


class MongoPipeline:
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        # Retrieve the MongoDB settings from the Scrapy settings
        mongo_uri = crawler.settings.get("MONGO_URI")
        mongo_db = crawler.settings.get("MONGO_DATABASE", "items")
        return cls(mongo_uri, mongo_db)

    def open_spider(self, spider):
        # Connect to MongoDB and select the database
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        # Use the spider's name to define the collection
        self.collection_name = f"{spider.name}_items"

    def close_spider(self, spider):
        # Close the MongoDB connection
        self.client.close()

    def process_item(self, item, spider):
        # Insert the item into the MongoDB collection
        self.db[self.collection_name].insert_one(ItemAdapter(item).asdict())
        return item
