# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field

class CartoonItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = Field()
    url = Field()
    webName = Field()
    hitNum = Field()
    commentNum = Field()
    collectionNum = Field()
    likeNum = Field()
    caiNum = Field()
    crawlTime = Field()
