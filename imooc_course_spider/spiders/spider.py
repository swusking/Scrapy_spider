#/usr/bin/env python
#coding:utf-8

import scrapy
from bs4 import BeautifulSoup as BS
from ..items import CourseItem, TeacherItem
from scrapy.http import Request, FormRequest        #Request模块
import copy, json, re


class MySpider(scrapy.Spider):
    name = 'imooc_course_spider'  #和entrypoint.py里的第三个参数一致
    base_url = 'http://www.imooc.com/course/list?page='

    def start_requests(self):
        for i in range(1, 31):
            url = self.base_url + str(i)
            yield Request(url=url, callback=self.get_classname)

    def get_classname(self, response):   #打印出课程名
        start_url = 'http://www.imooc.com/'
        html = response.text     #获取网页内容
        html_soup = BS(html, 'lxml')
        courses = html_soup.find_all(name='div', attrs={'class':'course-card-container'})  #获取全部课程的div框

        for course in courses:
            course_soup = BS(str(course), 'lxml')
            course_url = start_url + course_soup.a['href']   #拼接一下
            course_name_id = course_url.split('/')[-1]
            course_name = course_soup.h3.string
            yield Request(url=course_url, callback=self.get_class, meta={'url':course_url,
                                                                         'name':course_name,
                                                                         'name_id':course_name_id,
                                                                         })

    def get_class(self, response):

        ####实例化课程内容
        course_item = CourseItem()        #实例化
        course_item['name_id'] = response.meta['name_id']
        course_item['name'] = response.meta['name']
        course_item['url'] = response.meta['url']

        html = response.text
        html_soup = BS(html, 'lxml')
        static_items = html_soup.find_all(name='div', attrs={'class':re.compile('static-item l*')})
        # for static_item in static_items[1:]:
        #     soup = BS(str(static_item), 'lxml')
        #     print soup.div.contents[3].string
        course_item['difficulty'] = BS(str(static_items[1]), 'lxml').div.contents[3].string
        course_item['time'] = BS(str(static_items[2]), 'lxml').div.contents[3].string
        course_item['score'] = float(BS(str(static_items[3]), 'lxml').div.contents[3].string)


        #因为有些课程没有老师
        try:
            ######在这个页面上搜寻Teacher的主页
            teacher_info = html_soup.find_all(name='div', attrs={'class': 'teacher-info'})[0]
            teacher_soup = BS(str(teacher_info), 'lxml')

            teacher_name = teacher_soup.find_all(name='span', attrs={'class':'tit'})[0].a.string
            teacher_url = 'http://www.imooc.com' + teacher_soup.a['href']
            teacher_id = teacher_url.split('/')[4]
            teacher_content = teacher_soup.find_all(name='span', attrs={'class':'job'})[0].string
            teacher_content = teacher_content if teacher_content else u'无'

            #print teacher_name, teacher_content

        except BaseException, e:
            print '老师不存在'
            yield course_item   #没有老师则直接返回
        else:
        #这里必须为yield，不要就返回了
            yield course_item
            yield Request(url=teacher_url, callback=self.get_teacher, meta={'name':teacher_name,
                                                                            'id':teacher_id,
                                                                            'url':teacher_url,
                                                                            'content':teacher_content,
                                                                            })

    def get_teacher(self, response):
        teacher_item = TeacherItem()
        teacher_item['name_id'] = response.meta['id']
        teacher_item['name'] = response.meta['name']
        teacher_item['url'] = response.meta['url']
        teacher_item['content'] = response.meta['content']

        html_soup = BS(response.text, 'lxml')
        #高级讲师的页面会重定向到其他网址
        teacher_item['description'] = html_soup.find_all(name='p', attrs={'class':re.compile('(tea|user)-desc')})[0].string

        # print teacher_item
        return teacher_item

    def parse(self, response):    #只是一个回调作用，不要随意修改
        print response.status_code

