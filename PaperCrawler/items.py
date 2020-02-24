# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DataAboutPaper(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    authors=scrapy.Field()
    #Authors list Author //(AuthorName,AuthorUrl)
    pdfurl=scrapy.Field()
    #pdf download url
    abstract=scrapy.Field()
    timestamp=scrapy.Field()
    # Abstract String
    # conference=scrapy.Field() 
    main_subject=scrapy.Field()
    related_subject=scrapy.Field()

    it=scrapy.Field()
    # pass

class ConferenceItem(scrapy.Item):
    ConfID=scrapy.Field()
    ConfInstance=scrapy.Field()
    pass

class PaperItem(scrapy.Item):
    pass