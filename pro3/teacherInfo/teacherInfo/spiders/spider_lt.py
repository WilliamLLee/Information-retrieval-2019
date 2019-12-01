##############################
# spider for school of literature
# filename:spider_lt.py
# author:  liwei
# StuID:   1711350
# date:    2019.12.1
##############################

import scrapy
import os
from teacherInfo.items import TeacherinfoItem

class LTTeacherInfoSpider(scrapy.Spider):
    name = "lt"
    # 创建存储爬取信息的文件夹
    if not os.path.exists('../docs/%s'%name):
        os.mkdir('../docs/%s'%name)

    if not os.path.exists('../docs/%s/imgs' % name):
        os.mkdir('../docs/%s/imgs' % name)

    baseurl = 'http://wxy.nankai.edu.cn'

    img_name_dict = {}
    def start_requests(self):
        urls = [
            'https://wxy.nankai.edu.cn/zgyywxx/list1.htm',
            'https://wxy.nankai.edu.cn/zgyywxx/list2.htm',
            'https://wxy.nankai.edu.cn/cbxx/list.htm',
            'https://wxy.nankai.edu.cn/dfysx/list.htm',
            'https://wxy.nankai.edu.cn/yssjx/list.htm',
            'https://wxy.nankai.edu.cn/whszjxb/list.htm',
            'https://wxy.nankai.edu.cn/dzxg/list.htm',
            'https://wxy.nankai.edu.cn/xybgs/list.htm',
            'https://wxy.nankai.edu.cn/jxbgs/list.htm',
            'https://wxy.nankai.edu.cn/yjsbgs/list.htm',
            'https://wxy.nankai.edu.cn/syjxsfzx/list.htm',
            'https://wxy.nankai.edu.cn/tszlzx/list.htm',
            'https://wxy.nankai.edu.cn/wwxywhwbjb/list.htm'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        # 得到锚文本
        teacherItems = response.xpath('//table[@class ="wp_article_list_table"]')
        # 获取每位老师具体介绍页面链接锚文本
        nexturls = teacherItems.xpath('.//span[@class="Article_MicroImage"]')
        # 输出链接数据
        file = open('../docs/%s/index.txt'%self.name,'a',encoding='utf-8')
        for urlt in nexturls:
            print(urlt.get())
            file.write(urlt.xpath('.//a/@title').get()+","+urlt.xpath(".//a/@href").get()+'\n')
            #递归回调函数保存图片
            item = TeacherinfoItem()
            item['image_name'] = urlt.xpath('.//a/@title').get()
            item['image_url'] =self.baseurl+ urlt.xpath('.//img/@src').get()
            print( item['image_name'], item['image_url'])
            request = scrapy.Request(url=item['image_url'],callback=self.parseImg)
            request.meta['item']=item
            yield request
            # 递归回调解析教师信息的解析器
            yield scrapy.Request(url=urlt.xpath(".//a/@href").get(), callback=self.parseTeacher)
        file.close()

    def parseImg(self, response):
        item = response.meta['item']
        last = str(item['image_url']).split('.')[-1]
        if last == 'gif' :                  # gif格式为空的图片
            return
        with open('../docs/%s/imgs/%s.%s'%(self.name,item['image_name'],last),'wb') as f:
            f.write(response.body)
        f.close()

    def parseTeacher(self,response):
        #/html/body/div[3]/div/div/div
        details = response.xpath('//div[@class="article"]/div[@class="entry"]')
        filename = ''
        if details.xpath('.//div[@class = "basicInfo"]/h3/text()').get() is not None:
            filename = str(details.xpath('.//div[@class = "basicInfo"]/h3/text()').get()).replace('\n','').replace(' ','').replace('\r','')
        else:
            return
        f = open('../docs/%s/%s.txt'%(self.name,filename),'w',encoding='utf-8')
        f.write(filename+'\n')
        for item in details.xpath('.//div[@class = "basicInfo"]/p'):
            for text in item.xpath('.//text()').getall():
                f.write(str(text).replace('\n','').replace(' ','').replace('\r',''))
            f.write('\n')
        for item in details.xpath('.//div[@class = "otherInfo"]').xpath('.//p'):
            for text in item.xpath('.//text()').getall():
                f.write(str(text).replace('\n','').replace(' ','').replace('\r',''))
            f.write('\n')
        f.close()