##############################
# get data from source files
# filename:init.py
# author:  liwei
# StuID:   1711350
# date:    2019.12.5
##############################

import os
from shutil import copyfile
from sys import exit
import sys
import numpy as np

# 学院
xy_dict = {
    "南开大学商学院":"bs",
    "南开大学计算机学院":"cc",
    "南开大学经济学院":"ec",
    "南开大学历史学院":"ht",
    "南开大学法学院":"law",
    "南开大学文学院":"lt",
    "南开大学哲学院":"phi",
}

# 资源文档目录
file_path = '..\\docs'


# 获取某一人员的快照文件路径,相对于查询是的路由地址而言
def get_html(xueyuan,name):
    if os.path.exists("/snapshots/%s/%s.html"%(xy_dict[xueyuan],name)):
        return "/snapshots/%s/%s.html"%(xy_dict[xueyuan],name)
    else:
        return "/snapshots/%s/%s.html"%(xy_dict[xueyuan],str(name).replace(" ",""))


# 获取某一人员的内容文件路径
def get_content(xueyuan,name):
    if  os.path.exists( "../docs/%s/%s.txt"%(xy_dict[xueyuan],name)):      # 锚文本存储文件夹
        return "../docs/%s/%s.txt"%(xy_dict[xueyuan],name)
    else:
        return "../docs/%s/%s.txt"%(xy_dict[xueyuan],str(name).replace(" ",""))

# 获取某一人员的锚文本保存路径
def get_mtext(xueyuan,name):
    if  os.path.exists("../docs/%s/m_text/%s_m.txt"%(xy_dict[xueyuan],name)):      # 锚文本存储文件夹
        return "../docs/%s/m_text/%s_m.txt"%(xy_dict[xueyuan],name)
    else:
        return "../docs/%s/m_text/%s_m.txt"%(xy_dict[xueyuan],str(name).replace(" ",""))

# 获取某一人员的照片保存路径
def get_img(xueyuan,name):
    if  os.path.exists("../docs/%s/imgs/%s.jpg"%(xy_dict[xueyuan],str(name).replace(" ",""))):      # 锚文本存储文件夹
        return "../docs/%s/imgs/%s.jpg" % (xy_dict[xueyuan], name)
    elif  os.path.exists("../docs/%s/imgs/%s.png"%(xy_dict[xueyuan],str(name).replace(" ",""))):      # 锚文本存储文件夹
        return "../docs/%s/imgs/%s.png" % (xy_dict[xueyuan], name)
    elif os.path.exists("../docs/%s/imgs/%s.bmp"%(xy_dict[xueyuan],str(name).replace(" ",""))):      # 锚文本存储文件夹
        return "../docs/%s/imgs/%s.bmp" % (xy_dict[xueyuan], name)
    else:
        return "#"

# 获取所有的教师信息的index.txt 文件内容
def get_teacher_info():
    info = dict()
    # 遍历根目录对索引文本内容构建索引
    for root, dirs, files in os.walk(file_path, topdown=True):
        for file in files:
            path_t = os.path.join(root, file)
            if  path_t.split('\\')[-1] != 'index.txt':
                continue
            print("=======>" + path_t, file)
            f = open(path_t, 'r', encoding='UTF-8')
            for line in f:
                item_list = line.split(",")
                #print(item_list)
                #assert(item_list[0]+item_list[1] not in info.keys())     # 检验条件
                if item_list[0] in [x.split('-')[0] for x in   info.keys()]:
                    print("$$$$"+item_list[0]+item_list[1])                 # 存在同一个人，在不同的页面出现个人主页，且内容完全一样,只要链接不同，则视同为不同的人
                                                                            # 也有不同学院同名的，如果是同学院的同名情况则目前无法解决
                if item_list[0]+'-'+item_list[1] in info.keys():
                    print("####"+item_list[0]+item_list[1] )
                    pc = info[item_list[0]+'-'+item_list[1]]["pageRefer"]     # 同样的连接有两条指向存在，说明指向其锚文本数量为2，可用于连接分析
                    info[item_list[0] + '-' + item_list[1]]["pageRefer"]=pc+1
                    continue
                info[item_list[0]+'-'+item_list[1]] = {                      # 建立字典项
                    "name":item_list[0],
                    "url":item_list[1],
                    "xueyuan":item_list[2],
                    "parentUrl":item_list[3],
                    "pageRefer":1,
                }
    return info

# 转移图片
def move_img():
    # 遍历根目录将所有的图片转移到查询flask系统的静态目录下
    for root, dirs, files in os.walk(file_path, topdown=True):
        for file in files:
            path_t = os.path.join(root, file)
            if path_t.split('\\')[-2] != 'imgs':
                continue
            print("=======>" + path_t, file)
            source= path_t
            target = "./static/images/%s/%s"%(path_t.split('\\')[-3],path_t.split('\\')[-1])
            if not os.path.exists("./static/images/%s"%(path_t.split('\\')[-3])):
                os.makedirs("./static/images/%s"%(path_t.split('\\')[-3]))
            # adding exception handling
            try:
                copyfile(source, target)
            except IOError as e:
                print("Unable to copy file. %s" % e)
                exit(1)
            except:
                print("Unexpected error:", sys.exc_info())
                exit(1)



# 根据爬取的静态网页链接分析获取pagerank的值,info为获取的所有教师数据，info字段如下
# "name": item_list[0],
# "url": item_list[1],
# "xueyuan": item_list[2],
# "parentUrl": item_list[3],
# "pageRefer": 1,
def pagerank(info_t):
    info = dict(info_t)
    url_dict = dict()   # 存储网页编号映射关系
    url_pair = {}       # 存储网页指向对
    no = 0
    # 形成所有网页的序号映射表
    for key in info.keys():
        if info[key]["url"] not in url_dict.keys():
            url_dict[info[key]["url"]] = no
            no = no + 1
        if info[key]["parentUrl"] not in url_dict.keys():
            url_dict[info[key]["parentUrl"]] = no
            no = no + 1
        if info[key]["parentUrl"] not in url_pair.keys():
            url_pair[info[key]["parentUrl"]] = [info[key]["url"]]
        else:
            url_pair[info[key]["parentUrl"]].extend([info[key]["url"]])

    # 形成随机游走过程概率矩阵
    N = len(url_dict.keys())        # 矩阵规模
    matrix = np.zeros((N,N))        # 声明矩阵
    # 计算邻接矩阵
    for parenturl in url_pair.keys():
        for sonurl in url_pair[parenturl]:
            matrix[url_dict[parenturl]][url_dict[sonurl]] = 1
            matrix[url_dict[sonurl]][url_dict[parenturl]] = 0


    # 马尔科夫链 转移矩阵
    for i in range(N):
        count = 0
        for j in range(N):               # 统计1 的数量
            if matrix[i][j] ==1 :
                count=count +1
        if count == 0 :               # 一行中没有1 ，全部置位1/N
            for j in range(N):
                matrix[i][j] = 1.0/N
        else:
            for j in range(N):
                if matrix[i][j]==1:         # 非全0 替换为1/count
                    matrix[i][j]= 1.0/count
    alpha  =  0.1
    matrix1 = matrix*(1-alpha)
    matrix2 = matrix1+(alpha/N)
    # 设定初始的状态概率分布向量
    start = np.zeros((N,N))
    start[0][0] = 1
    cur = next = np.dot(start,matrix2)
    times = 0
    while(1):
        times =times+1
        exit_flag = True
        next = np.dot(cur,matrix2)     # 迭代

        for i in range(N):
            if next[0][i] != cur[0][i] :
                exit_flag = False
        if(exit_flag):
            break
        cur = next

    scores = next[0]
    print("end")
    return url_dict,scores              # 返回映射关系和page得分

print(pagerank(get_teacher_info()))

# 拷贝图片
# move_img()