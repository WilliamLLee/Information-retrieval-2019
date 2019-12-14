##############################
# spider for cs
# filename:spider_cc.py
# author:  liwei
# StuID:   1711350
# date:    2019.12.1
##############################

import scrapy
import os
snapshots_path = '../query_system/templates/snapshots'          # 网页快照保存位置

class CCTeacherInfoSpider(scrapy.Spider):
    name = "cc"
    # 创建存储爬取信息的文件夹
    if not os.path.exists('../docs/%s'%name):
        os.mkdir('../docs/%s'%name)

    if not os.path.exists('../docs/%s/m_text' % name):      # 锚文本存储文件夹
            os.mkdir('../docs/%s/m_text' % name)

    if not os.path.exists('%s/%s' % (snapshots_path,name)):      # 网页快照存储文件夹
            os.mkdir('%s/%s' % (snapshots_path,name))
    # if os.path.exists('../docs/%s/index.txt'%name):
    #     os.remove('../docs/%s/index.txt'%name)

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
            file.write(urlt.xpath('text()').get()+","+self.baseurl+urlt.xpath("@href").get()+","+"南开大学计算机学院"+","+response.url+'\n')
            # 保存锚文本
            m_f = open('../docs/%s/m_text/%s_m.txt' % (self.name, urlt.xpath('text()').get()), 'w', encoding='utf-8')
            m_f.write(str(urlt.get()))
            m_f.close()
            # 递归回调解析教师信息的解析器
            yield scrapy.Request(url=self.baseurl+urlt.xpath("@href").get(), callback=self.parseTeacher)
        file.close()


    def parseTeacher(self,response):
        details = response.xpath('//div[@class="body-introduce"]')

        filename = str(details.xpath('.//div[@class="form col-md-7"]/p[1]/span[2]/text()').get()).replace('\n','').replace(' ','').replace('\r','')

        # 保存网页快照
        with open('%s/%s/%s.html' % (snapshots_path, self.name, filename), 'wb')as s_f:
            s_f.write(response.body)
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
