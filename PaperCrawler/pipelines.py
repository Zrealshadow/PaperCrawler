# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from PaperCrawler.items import DataAboutPaper,ConferenceItem,PaperItem
class PapercrawlerPipeline(object):
    def __init__(self):
        pass
    def process_item(self, item, spider):
        if isinstance(item,DataAboutPaper):
            return item
        elif isinstance(item,ConferenceItem):
            return item
            pass
        elif isinstance(item,PaperItem):
            return item
            pass

    def close_spider(self,spider):
        pass

