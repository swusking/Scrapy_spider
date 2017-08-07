#/usr/bin/env python
#coding:utf-8

from .mysql import CourseSql, TeacherSql
from ..items import CourseItem, TeacherItem

class ScrapyTestPipeline(object):

    def process_item(self, item, spider):  #item和spider参数必须添加
        if isinstance(item, CourseItem):
            name_id = item['name_id']
            result = CourseSql.select_name(name_id)  #查找一下name_id是否存在
            if result[0] == 1:
                print '课程已经存在'
            else:
                name = item['name']
                url = item['url']
                difficulty = item['difficulty']
                time = item['time']
                score = item['score']
                CourseSql.insert_data(name_id, name, url, difficulty, time, score)
                print '已经存入数据库：', name

        if isinstance(item, TeacherItem):
            name_id = item['name_id']
            result = TeacherSql.select_name(name_id)  #查找一下name_id是否存在
            if result[0] == 1:
                print '老师存在'
            else:
                name = item['name']
                url = item['url']
                content = item['content']
                description = item['description']
                TeacherSql.insert_data(name_id, name, url, content, description)
                print '已经存入数据库：', name