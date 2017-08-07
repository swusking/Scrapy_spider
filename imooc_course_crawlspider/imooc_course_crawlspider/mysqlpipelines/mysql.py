#!/usr/bin/env python
#coding:utf-8

import MySQLdb
from imooc_course_crawlspider import settings

MYSQL_HOSTS = settings.MYSQL_HOSTS
MYSQL_USER = settings.MYSQL_USER
MYSQL_PASSWORD = settings.MYSQL_PASSWORD
MYSQL_PORT = settings.MYSQL_PORT
MYSQL_DB = settings.MYSQL_DB

db = MySQLdb.connect(MYSQL_HOSTS, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB, MYSQL_PORT, 'utf8')
cursor = db.cursor()
cursor.execute('SET NAMES utf8')        #没有会是乱码

class CourseSql:

    @classmethod    #不需要初始化类就可以调用类函数
    def insert_data(cls, name_id, name, url, difficulty, time, score):
        sql = 'INSERT INTO course(`name_id`, `name`, `url`, `difficulty`, `time`, `score`) VALUE (%s, %s, %s, %s, %s, %s)'
        cursor.execute(sql, (name_id, name.encode('utf-8'), url.encode('utf-8'), difficulty.encode('utf-8'), time.encode('utf-8'), score))
        db.commit()

    @classmethod
    def select_name(cls, name_id):  #用来去重
        sql = 'SELECT EXISTS (SELECT 1 FROM course WHERE `name_id` = %(name_id)s)'
        value = {'name_id':name_id}
        cursor.execute(sql, value)   #存在返回1，不存在返回0
        return cursor.fetchall()[0]


class TeacherSql:

    @classmethod    #不需要初始化类就可以调用类函数
    def insert_data(cls, name_id, name, url, content, description):
        sql = 'INSERT INTO teacher(`name_id`, `name`, `url`, `contents`, `description`) VALUE (%s, %s, %s, %s, %s)'
        #cursor.execute(sql, (name_id, '似懂非懂是', 'sking', '佛挡杀佛的', '佛挡杀佛'))
        cursor.execute(sql, (name_id, name.encode('utf-8'), url.encode('utf-8'), content.encode('utf-8'), description.encode('utf-8')))
        db.commit()

    @classmethod
    def select_name(cls, name_id):  #用来去重
        sql = 'SELECT EXISTS (SELECT 1 FROM teacher WHERE `name_id` = %(name_id)s)'
        value = {'name_id':name_id}
        cursor.execute(sql, value)   #存在返回1，不存在返回0
        return cursor.fetchall()[0]

