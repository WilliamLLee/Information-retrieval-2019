##############################
# spider for cs
# filename:spider_cc.py
# author:  liwei
# StuID:   1711350
# date:    2019.12.1
##############################

import scrapy
import os

class CCTeacherInfoSpider(scrapy.Spider):
    name = "cc"
    # 创建存储爬取信息的文件夹
    if not os.path.exists('../docs/%s'%name):
        os.mkdir('../docs/%s'%name)
    baseurl = 'https://cc.nankai.edu.cn/'
    def start_requests(self):
        urls = [
            'https://cc.nankai.edu.cn/jswyjy/list.htm',
            'https://cc.nankai.edu.cn/fjswfyjy/list.htm',
            'https://cc.nankai.edu.cn/js/list.htm',
            'https://cc.nankai.edu.cn/syjxdw/list.htm',

        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # 得到锚文本
        teacherItems = response.xpath('//table[@class="table table-striped table-bordered"]')
        # 获取每位老师具体介绍页面链接锚文本
        nexturls = teacherItems.css('a')
        # 输出链接数据
        file = open('../docs/%s/index.txt'%self.name,'a',encoding='utf-8')
        for urlt in nexturls:
            file.write(urlt.xpath('text()').get()+","+self.baseurl+urlt.xpath("@href").get()+'\n')
            # 递归回调解析教师信息的解析器
            yield scrapy.Request(url=self.baseurl+urlt.xpath("@href").get(), callback=self.parseTeacher)
        file.close()


    def parseTeacher(self,response):
        details = response.xpath('//div[@class="body-introduce"]')
        filename = str(details.xpath('.//div[@class="form col-md-7"]/p[1]/span[2]/text()').get()).replace('\n','').replace(' ','').replace('\r','')
        f = open('../docs/%s/%s.txt'%(self.name,filename),'w',encoding='utf-8')
        for item in details.xpath('.//div[@class="form col-md-7"]').css("p"):
            if item.css("span").get() is  None:
                if item.xpath("text()").get() is not None:
                    f.write(item.xpath("text()").get()+'\n')
            else:
                if item.xpath('./span[@class = "attribute"]/text()').get() is  not None  and item.xpath('./span[2]/text()').get()is  not None :
                    f.write(str(item.xpath('./span[@class = "attribute"]/text()').get()+item.xpath('./span[2]/text()').get()).replace('\n','').replace(' ','').replace('\r','')+"\n")
        for item in details.xpath('.//div[@id="PersonalProfile"]//p'):
            if item.get() is not  None:
                for text in item.xpath('.//text()').getall():
                    f.write(text)
                f.write('\n')
        f.close()
