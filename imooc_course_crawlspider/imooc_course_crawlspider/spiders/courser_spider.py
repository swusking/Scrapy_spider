#!/usr/bin/env python
#coding:utf-8

from scrapy.spiders import CrawlSpider, Rule, Request
from scrapy.linkextractors import LinkExtractor
from imooc_course_crawlspider.items import CourseItem, TeacherItem
from bs4 import BeautifulSoup


class MySpider(CrawlSpider):
    name = 'imooc_course_crawlspider'
    allowed_domains = ['imooc.com']
    start_urls = ['http://www.imooc.com/course/list/']

    rules = (
        Rule(LinkExtractor(allow=r'/course/list/\?page=\d+$')),
        Rule(LinkExtractor(allow=r'/learn/\d+$'), callback='course_item', follow=True),
        Rule(LinkExtractor(allow=r'/[ut]/\d+/courses\?sort=publish'), callback='teacher_item')
    )

    def course_item(self, response):
        courseItem = CourseItem()
        courseItem['name_id'] = int(response.url.split('/')[-1])
        courseItem['name'] = response.xpath('//*[@id="main"]/div[1]/div[1]/div[2]/h2/text()').extract()[0]
        courseItem['url'] = response.url
        courseItem['difficulty'] = response.xpath('//*[@id="main"]/div[1]/div[1]/div[3]/div[3]/span[2]/text()').extract()[0]
        courseItem['time'] = response.xpath('//*[@id="main"]/div[1]/div[1]/div[3]/div[4]/span[2]/text()').extract()[0]
        courseItem['score'] = float(response.xpath('//*[@id="main"]/div[1]/div[1]/div[3]/div[5]/span[2]/text()').extract()[0])

        return courseItem


    def teacher_item(self, response):
        teacherItem = TeacherItem()
        if response.url.split('/')[3] == 't':
            teacherItem['name_id'] = int(response.url.split('/')[4])
            teacherItem['name'] = response.xpath('//*[@id="main"]/div/div[1]/div[1]/div/div[2]/p[1]/text()').extract()[0]
            teacherItem['url'] = response.url
            try:
                teacherItem['content'] = response.xpath('//*[@id="main"]/div/div[1]/div[1]/div/div[2]/p[2]/text()').extract()[0]
            except BaseException, e:
                teacherItem['content'] = u''
            teacherItem['description'] = response.xpath('//*[@id="main"]/div/div[1]/div[1]/div/div[2]/p[3]/text()').extract()[0]
        if response.url.split('/')[3] == 'u':
            teacherItem['name_id'] = int(response.url.split('/')[4])
            teacherItem['name'] = response.xpath('//*[@id="main"]/div[1]/div/h3/span/text()').extract()[0]
            teacherItem['url'] = response.url
            teacherItem['description'] = response.xpath('//*[@id="main"]/div[1]/div/p[2]/text()').extract()[0]

            html_soup = BeautifulSoup(response.text, 'lxml')
            teacher_info = html_soup.find_all(name='p', attrs={'class':'about-info'})[0]
            #print teacher_info.span.next_sibling.string.strip().split(' ')[-1]
            teacherItem['content'] = teacher_info.span.next_sibling.string.strip().split(' ')[-1]


        return teacherItem