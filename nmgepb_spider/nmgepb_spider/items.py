#!/usr/bin/env python
#coding:utf-8

import scrapy

class Project_Item(scrapy.Item):
    name = scrapy.Field()
    location = scrapy.Field()
    company = scrapy.Field()
    organization = scrapy.Field()
    date = scrapy.Field()
    url = scrapy.Field()

