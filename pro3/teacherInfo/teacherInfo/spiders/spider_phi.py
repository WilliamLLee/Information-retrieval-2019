##############################
# spider for school of philosophy
# filename:spider_phi.py
# author:  liwei
# StuID:   1711350
# date:    2019.12.1
##############################

import scrapy
import os
from teacherInfo.items import TeacherinfoItem
import re
snapshots_path = '../query_system/templates/snapshots'          # 网页快照保存位置

class LTTeacherInfoSpider(scrapy.Spider):
    name = "phi"
    # 创建存储爬取信息的文件夹
    if not os.path.exists('../docs/%s'%name):
        os.mkdir('../docs/%s'%name)

    if not os.path.exists('../docs/%s/imgs' % name):
        os.mkdir('../docs/%s/imgs' % name)
    if not os.path.exists('../docs/%s/m_text' % name):      # 锚文本存储文件夹
            os.mkdir('../docs/%s/m_text' % name)

    if not os.path.exists('%s/%s' % (snapshots_path,name)):      # 网页快照存储文件夹
            os.mkdir('%s/%s' % (snapshots_path,name))
    # if os.path.exists('../docs/%s/index.txt'%name):
    #     os.remove('../docs/%s/index.txt'%name)


    baseurl = 'https://phil.nankai.edu.cn/'

    img_name_dict = {}
    def start_requests(self):
        urls = [
            'https://phil.nankai.edu.cn/ajyspx/list.htm'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parsePre)

    def parsePre(self, response):
        urls = response.xpath('//a[@class="col_name articlelist1_a_title "]/@href').getall()
        #print(urls)
        for nurl in urls:

            #print(self.baseurl+nurl)
            yield scrapy.Request(url=self.baseurl+nurl, callback=self.parse)

    def parse(self, response):
        # 得到锚文本
        teacherItems = response.xpath('//table[@class="article"]')
        print(teacherItems.get())
        # 获取每位老师具体介绍页面链接锚文本
        nexturls = teacherItems.xpath('.//a')
        for urlt in nexturls:
            nurl = str(urlt.xpath(".//@href").get()).replace('\n', '').replace(' ', '').replace('\r',
                                                                                                                 '').replace(
                '\t', '')
            # 存储锚文本
            item = {
                "m_text": urlt.get(),  # 锚文本
                "parentUrl": response.url,  # 父页面
                "xueyuan": "南开大学哲学院"  # 学院
            }
            #print(nurl)
            # 递归回调解析教师信息的解析器
            request = scrapy.Request(url=nurl, callback=self.parseTeacher)
            request.meta['item'] = item
            yield request

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
        data = response.meta['item']
        details = response.xpath('.//div[@frag="面板21"]')
        filename = details.xpath('.//table[1]/tr[1]/td/text()').get()
        print(filename)
        f = open('../docs/%s/%s.txt' % (self.name, filename), 'w', encoding='utf-8')
        f.write(filename + '\n')
        details = details.xpath('.//table[4]').xpath(".//table")
        for item in details.css('p'):
            print(item)
            for text in item.xpath('.//text()').getall():
                f.write(str(text).replace('\n', '').replace(' ', '').replace('\r', ''))
            f.write('\n')
        f.close()
        # 存儲映射信息
        file = open('../docs/%s/index.txt' % self.name, 'a', encoding='utf-8')
        file.write(filename + "," + response.url + ','+data["xueyuan"]+","+data['parentUrl']+'\n')
        file.close()
        # 保存锚文本
        m_f = open('../docs/%s/m_text/%s_m.txt' % (self.name, filename), 'w', encoding='utf-8')
        m_f.write(str(data["m_text"]))
        m_f.close()

        # 保存网页快照
        with open('%s/%s/%s.html' % (snapshots_path, self.name, filename), 'wb')as s_f:
            s_f.write(response.body)

        # 递归回调函数保存图片
        imgurl = details.xpath('.//td[@class="MsoNormal STYLE1"]').xpath('.//img/@src').get()
        print(imgurl)
        item = TeacherinfoItem()
        item['image_name'] = filename
        item['image_url'] = self.baseurl + imgurl
        # print(item['image_name'], item['image_url'])
        request = scrapy.Request(url=item['image_url'], callback=self.parseImg)
        request.meta['item'] = item
        yield request