#!/usr/bin/env python
#coding:utf-8

import csv, codecs
from items import Project_Item

class NmgepbSpiderPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, Project_Item):
            with open('project.csv', 'ab+') as csvfile:
                csvfile.write(codecs.BOM_UTF8)  # 防止中文乱码
                csvwriter = csv.writer(csvfile, dialect='excel')
                csvwriter.writerow([item['name'].encode('utf-8'), item['location'].encode('utf-8'), item['company'].encode('utf-8'),
                                    item['organization'].encode('utf-8'), item['date'].encode('utf-8'), item['url'].encode('utf-8')])  # 写入一行

