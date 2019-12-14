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
from data import xy_dict
from data import get_html,get_teacher_info,get_img,get_content,get_mtext

# 获取teacher index  info
info = get_teacher_info()

# 使用结巴中文分词
analyzer = ChineseAnalyzer()

# 资源文档目录
file_path = '..\\docs'

# 构建索引对象模型
schema = fields.Schema(title=TEXT(stored=True, analyzer=analyzer),                  # 姓名
                       url=ID(stored=True, analyzer=analyzer),                      # 链接
                       path=ID(stored=True, analyzer=analyzer),                     # 主页内容保存路径
                       content=TEXT(stored=True, analyzer=analyzer),                # 主页内容
                       mtext=TEXT(stored=True, analyzer=analyzer),                  # 锚文本
                       xueyuan=TEXT(stored=True, analyzer=analyzer),                # 学院
                       shotpath=TEXT(stored=True, analyzer=analyzer),               # 快照路径
                       picpath=TEXT(stored=True, analyzer=analyzer),                # 照片路径，如果不存在则为#
                       parenturl=TEXT(stored=True, analyzer=analyzer),              # 父亲链接
                        )

# 构建索引目录
if not os.path.exists('index'):             #如果目录index不存在则创建
    os.mkdir('index')
ix = index.create_in("index",schema)        #按照schema模式建立索引目录
ix = index.open_dir("index")                #打开该目录一遍存储索引文件

#索引构建，基于路径的基本索引
writer = ix.writer()
count = 0
# 遍历根目录对索引文本内容构建索引
for item in info.keys() :
    path_ct = get_content(info[item]['xueyuan'],info[item]["name"])
    path_mt = get_mtext(info[item]['xueyuan'],info[item]["name"])
    path_ht = get_html(info[item]['xueyuan'],info[item]["name"])
    path_img = get_img(info[item]['xueyuan'],info[item]["name"])
    print("=======>" + path_ct,path_ht,path_img,path_mt)
    # 获取信息文本
    content = ''
    if os.path.exists(path_ct):
        f = open(path_ct, 'r', encoding='UTF-8')
        for line in f:
            content = content + line
        f.close()
    # 获取锚文本
    m_text = ''
    if os.path.exists(path_mt):
        mf = open(path_mt, 'r', encoding='UTF-8')
        for line in mf:
            m_text = m_text + line
        mf.close()

    writer.add_document(title=info[item]['name'],
                        url=info[item]['url'],
                        content=content,
                        path=path_ct,
                        mtext=m_text,
                        xueyuan=info[item]['xueyuan'],
                        shotpath= path_ht,
                        picpath= path_img,
                        parenturl=info[item]['parentUrl'],
                        )
    count = count + 1
writer.commit()
print("==========>共索引文件%d个"%count)




# #索引构建，基于路径的基本索引
# writer = ix.writer()
# count = 0
# # 遍历根目录对索引文本内容构建索引
# for root, dirs, files in os.walk(file_path, topdown=True):
#     for file in files:
#         path_t = os.path.join(root, file)
#         if path_t.split('.')[-1] != 'txt' or path_t.split('\\')[-1] =='index.txt':
#             continue
#         print("=======>"+path_t,file)
#         f = open( path_t, 'r', encoding='UTF-8')
#         content = ''
#         for line in f:
#             content = content + line
#         writer.add_document(title=file, content=content, path= path_t)
#         count =count+1
# writer.commit()
# print("==========>共索引文件%d个"%count)




#查询构建，测试索引构建的效果

from whoosh.qparser import QueryParser
with ix.searcher() as searcher:
    query = QueryParser("content",ix.schema).parse("信息检索")
    result = searcher.search(query)
    for item in result:
        print(item)
    print(len(result))