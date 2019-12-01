##############################
# spider for school of history
# filename:spider_ht.py
# author:  liwei
# StuID:   1711350
# date:    2019.12.1
##############################

import scrapy
import os
from teacherInfo.items import TeacherinfoItem
import re

class HTTeacherInfoSpider(scrapy.Spider):
    name = "ht"
    # 创建存储爬取信息的文件夹
    if not os.path.exists('../docs/%s'%name):
        os.mkdir('../docs/%s'%name)

    if not os.path.exists('../docs/%s/imgs'%name):
        os.mkdir('../docs/%s/imgs'%name)

    baseurl = 'https://history.nankai.edu.cn/'

    img_name_dict = {}
    def start_requests(self):
        urls = [
            'https://history.nankai.edu.cn/16054/list.htm',
            'https://history.nankai.edu.cn/16055/list.htm',
            'https://history.nankai.edu.cn/16056/list.htm',
            'https://history.nankai.edu.cn/16053/list.htm'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        # 得到锚文本
        teacherItems = response.xpath('//div[@frag="窗口44"]')
        # 获取每位老师具体介绍页面链接锚文本
        nexturls = teacherItems.xpath('.//li[@class="teacher_list_unit cl"]')
        for urlt in nexturls:
            nurl = str(self.baseurl+urlt.xpath(".//a/@href").get()).replace('\n','').replace(' ','').replace('\r','').replace('\t','')
            # 递归回调解析教师信息的解析器
            yield scrapy.Request(url=nurl, callback=self.parseTeacher)

    def parseImg(self, response):
        item = response.meta['item']
        last = str(item['image_url']).split('.')[-1]
        #if last == 'gif' :                  # gif格式为空的图片
        #    return
        with open('../docs/%s/imgs/%s.%s'%(self.name,item['image_name'],last),'wb') as f:
            f.write(response.body)
        f.close()

    def parseTeacher(self,response):
        #/html/body/div[3]/div/div/div
        details = response.xpath('//div[@class="leader-list leader cl"]/div[@class="wp_articlecontent"]')
        splitwords = re.findall(r'[\u4e00-\u9fa5]*|[a-zA-Z]*',str(details.xpath('.//div[@class = "info"]/div[@class="name"]/text()').get()))
        filename=''
        for p in [x for x in splitwords if len(x)>=1]:
            filename =filename+p
        f = open('../docs/%s/%s.txt'%(self.name,filename),'w',encoding='utf-8')
        f.write(filename+'\n')
        for item in details.xpath('.//div[@class = "info"]').xpath('.//div[@class="label-value"]'):
            print(item)
            for text in item.xpath('.//text()').getall():
                f.write(str(text).replace('\n','').replace(' ','').replace('\r',''))
            f.write('\n')
        for item in details.xpath('.//div[@id="tabsDiv"]').css('p'):
            print(item)
            for text in item.xpath('.//text()').getall():
                f.write(str(text).replace('\n','').replace(' ','').replace('\r',''))
            f.write('\n')
        f.close()
        # 存儲映射信息
        file = open('../docs/%s/index.txt'%self.name,'a',encoding='utf-8')
        file.write(filename+ "," + response.url+ '\n')
        file.close()
        # 递归回调函数保存图片
        imgurl = details.xpath('.//img/@src').get()
        item = TeacherinfoItem()
        item['image_name'] = filename
        item['image_url'] = self.baseurl + imgurl
        #print(item['image_name'], item['image_url'])
        request = scrapy.Request(url=item['image_url'], callback=self.parseImg)
        request.meta['item'] = item
        yield request