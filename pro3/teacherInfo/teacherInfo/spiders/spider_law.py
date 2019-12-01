##############################
# spider for school of law
# filename:spider_law.py
# author:  liwei
# StuID:   1711350
# date:    2019.12.1
##############################

import scrapy
import os
from teacherInfo.items import TeacherinfoItem
import re

class LTTeacherInfoSpider(scrapy.Spider):
    name = "law"
    # 创建存储爬取信息的文件夹
    if not os.path.exists('../docs/%s'%name):
        os.mkdir('../docs/%s'%name)

    if not os.path.exists('../docs/%s/imgs' % name):
        os.mkdir('../docs/%s/imgs' % name)

    baseurl = 'http://law.nankai.edu.cn/'

    img_name_dict = {}
    def start_requests(self):
        urls = [
            'http://law.nankai.edu.cn/4912/list.htm'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # 得到锚文本
        teacherItems = response.xpath('/html/body/div[4]/div/div/div[3]/div[3]/div')
        #print(teacherItems.get())
        # 获取每位老师具体介绍页面链接锚文本
        nexturls = teacherItems.xpath('.//span[@ class="Article_Title"]')
        for urlt in nexturls:
            nurl = str(urlt.xpath(".//a/@href").get()).replace('\n', '').replace(' ', '').replace('\r',
                                                                                                                 '').replace(
                '\t', '')
            #print(nurl)
            # 递归回调解析教师信息的解析器
            yield scrapy.Request(url=self.baseurl+nurl, callback=self.parseTeacher)

    def parseImg(self, response):
        item = response.meta['item']
        last = str(item['image_url']).split('.')[-1]
        # if last == 'gif' :                  # gif格式为空的图片
        #    return
        with open('../docs/%s/imgs/%s.%s' % (self.name, item['image_name'], last), 'wb') as f:
            f.write(response.body)
        f.close()

    def parseTeacher(self, response):
        # /html/body/div[3]/div/div/div
        details = response.xpath('.//div[@class="article"]')
        filename = details.xpath('.//h1 [@class="arti_title"]/text()').get()
        print(filename)
        f = open('../docs/%s/%s.txt' % (self.name, filename), 'w', encoding='utf-8')
        f.write(filename + '\n')
        details = details.xpath('.//div[@class="entry"]')
        for item in details.css('p'):
            print(item)
            for text in item.xpath('.//text()').getall():
                f.write(str(text).replace('\n', '').replace(' ', '').replace('\r', ''))
            f.write('\n')
        f.close()
        # 存儲映射信息
        file = open('../docs/%s/index.txt' % self.name, 'a', encoding='utf-8')
        file.write(filename + "," + response.url + '\n')
        file.close()
        # 递归回调函数保存图片
        imgurl = details.xpath('.//img/@src').get()
        print(imgurl)
        item = TeacherinfoItem()
        item['image_name'] = filename
        item['image_url'] = self.baseurl + imgurl
        # print(item['image_name'], item['image_url'])
        request = scrapy.Request(url=item['image_url'], callback=self.parseImg)
        request.meta['item'] = item
        yield request