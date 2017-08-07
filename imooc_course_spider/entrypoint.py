#/usr/bin/env python
#coding:utf-8

from scrapy.cmdline import execute
execute(['scrapy', 'crawl', 'imooc_course_spider'])    #前两个固定，后面的是spiders的name参数