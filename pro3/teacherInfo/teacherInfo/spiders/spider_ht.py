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
snapshots_path = '../query_system/templates/snapshots'          # 网页快照保存位置

class HTTeacherInfoSpider(scrapy.Spider):
    name = "ht"
    # 创建存储爬取信息的文件夹
    if not os.path.exists('../docs/%s'%name):
        os.mkdir('../docs/%s'%name)

    if not os.path.exists('../docs/%s/imgs'%name):
        os.mkdir('../docs/%s/imgs'%name)
    if not os.path.exists('../docs/%s/m_text' % name):      # 锚文本存储文件夹
            os.mkdir('../docs/%s/m_text' % name)


    if not os.path.exists('%s/%s' % (snapshots_path,name)):      # 网页快照存储文件夹
            os.mkdir('%s/%s' % (snapshots_path,name))
    # if os.path.exists('../docs/%s/index.txt'%name):
    #     os.remove('../docs/%s/index.txt'%name)

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
            # 存储锚文本
            item = {
                "m_text": urlt.get(),  # 锚文本
                "parentUrl": response.url,  # 父页面
                "xueyuan": "南开大学历史学院"  # 学院
            }

            # 递归回调解析教师信息的解析器
            request = scrapy.Request(url=nurl, callback=self.parseTeacher)
            request.meta['item'] = item
            yield request

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
        data = response.meta['item']

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
        file.write(filename+ "," + response.url+','+data["xueyuan"]+","+data['parentUrl']+  '\n')
        file.close()


        # 保存网页快照
        with open('%s/%s/%s.html' % (snapshots_path, self.name, filename), 'wb')as s_f:
            s_f.write(response.body)

        # 保存锚文本
        m_f = open('../docs/%s/m_text/%s_m.txt' % (self.name, filename), 'w', encoding='utf-8')
        m_f.write(str(data["m_text"]))
        m_f.close()

        # 递归回调函数保存图片
        imgurl = details.xpath('.//img/@src').get()
        item = TeacherinfoItem()
        item['image_name'] = filename
        item['image_url'] = self.baseurl + imgurl
        #print(item['image_name'], item['image_url'])
        request = scrapy.Request(url=item['image_url'], callback=self.parseImg)
        request.meta['item'] = item
        yield request