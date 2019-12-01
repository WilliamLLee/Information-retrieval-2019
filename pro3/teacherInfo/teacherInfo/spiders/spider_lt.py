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

class CCTeacherInfoSpider(scrapy.Spider):
    name = "lt"
    # 创建存储爬取信息的文件夹
    if not os.path.exists('../docs/%s'%name):
        os.mkdir('../docs/%s'%name)
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
        #file = open('../../../docs/%s/index.txt'%self.name,'a',encoding='utf-8')
        for urlt in nexturls:
            print(urlt.get())
            #file.write(urlt.xpath('.//a/@title').get()+","+urlt.xpath(".//a/@href").get()+'\n')
            #递归回调函数保存图片
            item['image_urls'] = urlt.xpath('.//img/@src').get()
            #print("a"+self.baseurl + imgurl)
            #self.img_name_dict[self.baseurl + imgurl]=urlt.xpath('.//a/@title').get()
            #yield scrapy.Request(url=self.baseurl + imgurl,callback=self.parseImg)
            # 递归回调解析教师信息的解析器
            #yield scrapy.Request(url=urlt.xpath(".//a/@href").get(), callback=self.parseTeacher)
        #file.close()

    def parseImg(self, response):
        print('b'+response.url)
       # print(self.img_name_dict)
        imgpath = ''
        if response.url in self.img_name_dict.keys():
            imgpath = '../../../docs/%s/imgs/%s.%s' % (self.name,self.img_name_dict[response.url], str(response.url).split('.')[-1])
        else:
            return
        with  open(imgpath, 'wb') as img:
            img.write(response.body)
        img.close()


    def parseTeacher(self,response):
        #/html/body/div[3]/div/div/div
        details = response.xpath('//div[@class="article"]/div[@class="entry"]')
        filename = ''
        if details.xpath('.//div[@class = "basicInfo"]/h3/text()').get() is not None:
            filename = str(details.xpath('.//div[@class = "basicInfo"]/h3/text()').get()).replace('\n','').replace(' ','').replace('\r','')
        else:
            return
        f = open('../../../docs/%s/%s.txt'%(self.name,filename),'w',encoding='utf-8')
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