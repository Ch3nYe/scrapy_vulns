# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScarpyVulnsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    time = scrapy.Field()
    title = scrapy.Field()
    rank = scrapy.Field()
    author = scrapy.Field()
    organization = scrapy.Field()
    type = scrapy.Field()
