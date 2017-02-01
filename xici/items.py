# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class XiciItem(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    inputtime = scrapy.Field()
    #pass


class ProxyItem(scrapy.Item):
    ip = scrapy.Field()
    port = scrapy.Field()
    position = scrapy.Field()
    http_type = scrapy.Field()
    speed = scrapy.Field()
    connect_time = scrapy.Field()
    check_time = scrapy.Field()
    error_time = scrapy.Field()