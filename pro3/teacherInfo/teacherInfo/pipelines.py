# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.pipelines.images import ImagesPipeline
import os
from teacherInfo.settings import IMAGES_STORE as image_store

class TeacherinfoPipeline(ImagesPipeline):
    def process_item(self, item, spider):
        return item

    def get_media_requests(self, item, info):
        # 发起壁纸下载请求
        yield scrapy.Request(item['image_url'])

    def item_completed(self, results, item, info):
        # 对壁纸进行重命名
        os.rename(image_store + '/' + results[0][1]['path'], image_store + '/' + item['image_name'] + '.jpg')

    def __del__(self):
        # 完成后删除full目录
        os.removedirs(image_store + '/' + 'full')

