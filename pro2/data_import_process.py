# date: 2019年10月28日
# author: lw
# e-mail: lio6218@163.com
# description: 本文件主要实现导入数据的模块和生成编号映射关系文件函数,
#              在编号的同时将繁体字转为简体字，导出的诗文文本json文件存在create文件夹中

import json
import zhconv

# 作者信息存储路径
authors_tang_path = "./chinesepoetry/authors.tang.json"
authors_song_path = "./chinesepoetry/authors.song.json"
# 输出的json文件存储路径
create_path = "./create"

# 给诗文和作者信息转为简体字，同时将生成的结果存入新的文件目录下
# path为新的路径
# 作者信息格式为： 作者 描述
# 诗文编号信息格式为： 作者 诗名 诗文
def convert_poets_lang():
    # 唐朝诗人信息
    load_f_t = open(authors_tang_path, 'r', encoding="UTF-8")
    t_dump = open("./create/tang/authors.json",'w',encoding="UTF-8")
    authors_t = json.load(load_f_t)
    info_list_t = []
    for item in authors_t:
        info_list_t.append({"name":zhconv.convert(item["name"], 'zh-cn'),"desc":zhconv.convert(item["desc"], 'zh-cn')})
    json.dump(info_list_t,t_dump,indent=4,ensure_ascii=False)
    t_dump.close()
    print("--------》》》》唐朝诗人信息处理完毕")
    # 宋朝诗人信息
    load_f_s = open(authors_song_path, 'r', encoding="UTF-8")
    s_dump = open("./create/song/authors.json", 'w', encoding="UTF-8")
    authors_s = json.load(load_f_s)
    info_list_s = []
    for item in authors_s:
        info_list_s.append({"name":zhconv.convert(item["name"], 'zh-cn'),"desc":zhconv.convert(item["desc"], 'zh-cn')})
    json.dump(info_list_s, s_dump, indent=4,ensure_ascii=False)
    s_dump.close()
    print("--------》》》》宋朝诗人信息处理完毕")
    # 宋朝诗文
    for j in range(0,255):
        poets_list = []
        f = open("./chinesepoetry/poet.song.%d.json"%(j*1000),'r',encoding="UTF-8")
        dump_f = open("./create/song/%d.json"%(j*1000),'w',encoding="UTF-8")
        temp = json.load(f)
        for k  in range(len(temp)):
            poets_text = ""
            for item in temp[k]["paragraphs"]:
                poets_text+=zhconv.convert(item,'zh-cn')
            poets_list.append({"author":zhconv.convert(temp[k]["author"],'zh-cn'),"title":zhconv.convert(temp[k]["title"],'zh-cn'),
                               "paragraphs":poets_text})
        json.dump(poets_list, dump_f, indent=4,ensure_ascii=False)
        print(j)
        dump_f.close()
    print("--------》》》》唐朝诗文处理完毕")
    # 唐朝诗文
    for j in range(0,58):
        poets_list = []
        f = open("./chinesepoetry/poet.tang.%d.json"%(j*1000),'r',encoding="UTF-8")
        dump_f = open("./create/tang/%d.json" % (j * 1000), 'w', encoding="UTF-8")
        temp = json.load(f)
        f.close()
        for k  in range(len(temp)):
            poets_text = ""
            for item in temp[k]["paragraphs"]:
                poets_text += zhconv.convert(item, 'zh-cn')
            poets_list.append({"author": zhconv.convert(temp[k]["author"], 'zh-cn'),
                               "title": zhconv.convert(temp[k]["title"], 'zh-cn'),
                               "paragraphs": poets_text})
        json.dump(poets_list,dump_f,indent=4,ensure_ascii=False)
        dump_f.close()
        print(j)
    print("--------》》》》宋朝诗文处理完毕")

# 按照编号顺序导入诗文,直接导入简体版本
# 返回值为诗文的总量count ,和诗文正文的列表 poets
def import_poets():
    count = 0
    poets = []
    for j in range(0,255):
        f = open("./create/song/%d.json"%(j*1000),'r',encoding="UTF-8")
        temp = json.load(f)
        for k  in range(len(temp)):
            poets.append(temp[k]["paragraphs"])
            count = count + 1
    for j in range(0,58):
        f = open("./create/tang/%d.json"%(j*1000),'r',encoding="UTF-8")
        temp = json.load(f)
        for k  in range(len(temp)):
            poets.append(temp[k]["paragraphs"])
            count = count + 1
    return count,poets

# 读取作者信息，返回一个列表
# path 为诗人信息的存储文件
# 返回值authors为诗人信息列表
def import_authors(path):
    load_f = open(path,'r',encoding="UTF-8")
    authors = json.load(load_f)
    return authors


# 测试调用

# print(len(import_authors(authors_song_path)))
# list_poets(out_list_file_path)

# poets_count,poets = import_poets()
# print(poets_count)
# print(poets)
# convert_poets_lang()
# print(import_poets())