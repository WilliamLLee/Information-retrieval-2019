# date: 2019年10月28日
# author: 李伟
# e-mail: lio6218@163.com
# description: 本文件主要实现导入数据的模块和生成编号映射关系文件函数

import json

# 作者信息存储路径
authors_tang_path = "./chinesepoetry/authors.tang.json"
authors_song_path = "./chinesepoetry/authors.song.json"
# 输出诗文信息编号的json文件路径
out_list_file_path = "./create/list_info.json"

# 读取作者信息，返回一个列表
# path 为诗人信息的存储文件
# 返回值authors为诗人信息列表
def import_authors(path):
    authors = {}       # 诗人信息字典
    load_f = open(path,'r',encoding="UTF-8")
    authors = json.load(load_f)
    return authors

# 给诗文编号，并对应上相应文件和在文件存储的列表中的下标号
# 由于文件名的规范，因此不需要记录路径了，记录为唐诗还是宋词即可
# out_list_file 为输出编号信息的列表
# 编号信息格式为： 编号  朝代（t/s） 列表下标 作者 诗名
def list_poets(out_list_file):
    poets_list = []
    i = 0
    for j in range(0,255):
        f = open("./chinesepoetry/poet.song.%d.json"%(j*1000),'r',encoding="UTF-8")
        temp = json.load(f)
        for k  in range(len(temp)):
            poets_list.append({"no":i,"dynasty":"t","list_no":k,"author":temp[k]["author"],"title":temp[k]["title"]})
            i = i+1
        print(j)
    for j in range(0,58):
        f = open("./chinesepoetry/poet.tang.%d.json"%(j*1000),'r',encoding="UTF-8")
        temp = json.load(f)
        for k  in range(len(temp)):
            poets_list.append({"no":i,"dynasty":"s","list_no":k,"author":temp[k]["author"],"title":temp[k]["title"]})
            i = i+1
        print(j)
    dump_f = open(out_list_file,'w',encoding="UTF-8")
    json.dump(poets_list,dump_f)
    print(poets_list)

# 按照编号顺序导入诗文
# 返回值为诗文的总量count ,和诗文正文的列表 poets
def import_poets():
    count = 0
    poets = []
    for j in range(0,255):
        f = open("./chinesepoetry/poet.song.%d.json"%(j*1000),'r',encoding="UTF-8")
        temp = json.load(f)
        for k  in range(len(temp)):
            poets.append(temp[k]["paragraphs"])
            count = count + 1
    for j in range(0,58):
        f = open("./chinesepoetry/poet.tang.%d.json"%(j*1000),'r',encoding="UTF-8")
        temp = json.load(f)
        for k  in range(len(temp)):
            poets.append(temp[k]["paragraphs"])
            count = count + 1
    return count,poets


# 测试调用

# print(len(import_authors(authors_song_path)))
# list_poets(out_list_file_path)

# poets_count,poets = import_poets()
# print(poets_count)
# print(poets)