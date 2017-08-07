# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CourseItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name_id = scrapy.Field()
    name = scrapy.Field()
    url = scrapy.Field()
    difficulty = scrapy.Field()
    time = scrapy.Field()
    score = scrapy.Field()

class TeacherItem(scrapy.Item):
    name_id = scrapy.Field()
    name = scrapy.Field()
    url = scrapy.Field()
    content = scrapy.Field()
    description = scrapy.Field()

