##############################
# spider for school of economic
# filename:spider_ec.py
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
    name = "ec"
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

    baseurl = 'http://fcollege.nankai.edu.cn/'

    img_name_dict = {}
    def start_requests(self):
        urls = [
            'https://economics.nankai.edu.cn/gdrc/list.htm',
            'https://economics.nankai.edu.cn/qzjs/list.htm',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parseTeacher)
        yield scrapy.Request(url='https://economics.nankai.edu.cn/jzjs/list.htm', callback=self.parseTeacher2)

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
        details = response.xpath('.//div[@class="brief"]')
        for temp in details:
            filename = temp.xpath('.//div/p[1]/text()').get()
            # 保存网页快照
            with open('%s/%s/%s.html' % (snapshots_path, self.name, filename), 'wb')as s_f:
                s_f.write(response.body)
            print(filename)
            f = open('../docs/%s/%s.txt' % (self.name, filename), 'w', encoding='utf-8')
            f.write(filename + '\n')
            imgurl = temp.xpath('.//img/@src').get()
            temp = temp.xpath('.//div[@class="intro"]')
            for item in temp.css('p'):
                print(item)
                for text in item.xpath('.//text()').getall():
                    f.write(str(text).replace('\n', '').replace(' ', '').replace('\r', ''))
                f.write('\n')
            f.close()
            # 存儲映射信息
            file = open('../docs/%s/index.txt' % self.name, 'a', encoding='utf-8')
            file.write(filename + "," + response.url+","+"南开大学经济学院"+","+response.url+ '\n')
            file.close()
            # 保存锚文本
            m_f = open('../docs/%s/m_text/%s_m.txt' % (self.name, filename ), 'w', encoding='utf-8')
            m_f.write(str( temp.get()))
            m_f.close()

            # 递归回调函数保存图片
            if imgurl is None:
                continue
            print(imgurl)
            item = TeacherinfoItem()
            item['image_name'] = filename
            item['image_url'] = self.baseurl + imgurl
            # print(item['image_name'], item['image_url'])
            request = scrapy.Request(url=item['image_url'], callback=self.parseImg)
            request.meta['item'] = item
            yield request

    def parseTeacher2(self, response):
        # /html/body/div[3]/div/div/div
        details = response.xpath('.//div[@class="jz_li_div"]')
        for temp in details:
            filename = temp.xpath('.//h3/text()').get()
            # 保存网页快照
            with open('%s/%s/%s.html' % (snapshots_path, self.name, filename), 'wb')as s_f:
                s_f.write(response.body)

            print(filename)
            f = open('../docs/%s/%s.txt' % (self.name, filename), 'w', encoding='utf-8')
            f.write(filename + '\n')
            imgurl = temp.xpath('.//img/@src').get()
            temp = temp.xpath('.//div[@class="jz_li_content"]')
            for item in temp.css('p'):
                print(item)
                for text in item.xpath('.//text()').getall():
                    f.write(str(text).replace('\n', '').replace(' ', '').replace('\r', ''))
                f.write('\n')
            f.close()
            # 存儲映射信息
            file = open('../docs/%s/index.txt' % self.name, 'a', encoding='utf-8')
            file.write(filename + "," + response.url +","+"南开大学经济学院"+","+response.url+ '\n')
            file.close()

            # 保存锚文本
            m_f = open('../docs/%s/m_text/%s_m.txt' % (self.name, filename), 'w', encoding='utf-8')
            m_f.write(str(temp.get()))
            m_f.close()
            # 递归回调函数保存图片
            if imgurl is None:
                continue
            print(imgurl)
            item = TeacherinfoItem()
            item['image_name'] = filename
            item['image_url'] = self.baseurl + imgurl
            # print(item['image_name'], item['image_url'])
            request = scrapy.Request(url=item['image_url'], callback=self.parseImg)
            request.meta['item'] = item
            yield request