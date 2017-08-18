#!/usr/bin/env python
#coding:utf-8

import scrapy
from scrapy.http import Request
from ..items import Project_Item
from bs4 import BeautifulSoup
import csv, codecs

class Nmagepb_Spider(scrapy.Spider):
    name = 'nmgepb_spider'
    base_url = 'http://www.nmgepb.gov.cn/ywgl/hjpj/xmslqk/'

    def start_requests(self):
        with open('project.csv', 'wb') as csvfile:
            csvfile.write(codecs.BOM_UTF8)  # 防止中文乱码
            csvwriter = csv.writer(csvfile, dialect='excel')
            csvwriter.writerow(['name', 'location', 'company', 'organization', 'date', 'url'])

        for i in range(0, 6):
            if i == 0:
                url = self.base_url + 'index' + '.html'
            else:
                url = self.base_url + 'index_' + str(i) + '.html'
            yield Request(url=url, callback=self.get_project_url)

    def get_project_url(self, response):
        html_soup = BeautifulSoup(response.text, 'lxml')
        li_list = html_soup.find_all(name='li', attrs={'style':' width:820px; height:40px;line-height: 40px;'})
        for li in li_list:
            url = self.base_url + li.span.next_sibling.a['href'][2:]
            yield Request(url=url, callback=self.get_project_info)

    def get_project_info(self, response):
        project_item = Project_Item()

        html_soup = BeautifulSoup(response.text, 'lxml')
        p = html_soup.find_all(name='p', attrs={'sizset':'false'})
        if p:
            p = p[0]
            project_info = []
            for string in p.stripped_strings:
                project_info.append(string)
            try:
                project_item['name'] = project_info[8]
                project_item['location'] = project_info[10]
                project_item['company'] = project_info[12]
                project_item['organization'] = project_info[14]
                project_item['date'] = project_info[16]
                project_item['url'] = response.url
                return project_item

            except BaseException, e:
                print e


