##############################
# init index dir and make index for files
# filename:init.py
# author:  liwei
# StuID:   1711350
# date:    2019.12.5
##############################

import os
from whoosh import fields
from whoosh import index
from whoosh.fields import *
from jieba.analyse import ChineseAnalyzer

# 使用结巴中文分词
analyzer = ChineseAnalyzer()

# 资源文档目录
file_path = '..\\docs'

# 构建索引对象模型
schema = fields.Schema(title=TEXT(stored=True, analyzer=analyzer), path=ID(stored=True, analyzer=analyzer), content=TEXT(stored=True, analyzer=analyzer))

# 构建索引目录
if not os.path.exists('index'):             #如果目录index不存在则创建
    os.mkdir('index')
ix = index.create_in("index",schema)        #按照schema模式建立索引目录
ix = index.open_dir("index")                #打开该目录一遍存储索引文件

#索引构建
writer = ix.writer()
count = 0
# 遍历根目录对索引文本内容构建索引
for root, dirs, files in os.walk(file_path, topdown=True):
    for file in files:
        path_t = os.path.join(root, file)
        if path_t.split('.')[-1] != 'txt' or path_t.split('\\')[-1] =='index.txt':
            continue
        print("=======>"+path_t,file)
        f = open( path_t, 'r', encoding='UTF-8')
        content = ''
        for line in f:
            content = content + line
        writer.add_document(title=file, content=content, path= path_t)
        count =count+1
writer.commit()
print("==========>共索引文件%d个"%count)


#查询构建，测试索引构建的效果
from whoosh.qparser import QueryParser
with ix.searcher() as searcher:
    query = QueryParser("content",ix.schema).parse("信息")
    result = searcher.search(query)
    for item in result:
        print(item)
    print(len(result))