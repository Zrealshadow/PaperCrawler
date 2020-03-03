# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json
from PaperCrawler.items import DataAboutPaper,ConferenceItem,PaperItem
class PapercrawlerPipeline(object):
    # def __init__(self):
    #     pass
    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        if isinstance(item,DataAboutPaper):
            return item
        elif isinstance(item,ConferenceItem):
            self.conffile.write(line)
            # return item
        elif isinstance(item,PaperItem):
            self.paperfile.write(line)
            # return item

    def open_spider(self,spider):
        # self.conffile=open("./output/confitem.json",'w')
        # self.paperfile=open("./output/paperitem.json",'w')
        self.conffile=open("./output/confBitem.json",'w')
        self.paperfile=open("./output/paperBitem.json",'w')

    def close_spider(self,spider):
        self.conffile.close()
        self.paperfile.close()

