#!/usr/bin/python
# coding:utf-8

import scrapy


class RmrbSqliteItem(scrapy.Item):
    title = scrapy.Field()
    publish = scrapy.Field()
    text = scrapy.Field()
    link = scrapy.Field()
    pass
