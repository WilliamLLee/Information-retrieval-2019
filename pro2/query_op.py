# date: 2019年11月1日
# author: lw
# e-mail: lio6218@163.com
# description: 本文件主要实现基于位置索引和双字索引的诗文查询函数，返回匹配的结果

from  data_import_process import import_d_index  # 引入双字索引导入函数
from data_import_process import import_p_index # 引入位置所引导入函数
# from data_import_process import import_poets
from data_import_process import import_author_title_index
from data_import_process import import_poets_info
# 导入索引
author_index, title_index = import_author_title_index()
double_index = import_d_index()
position_index = import_p_index()
# count,poets = import_poets()
count,poets_info = import_poets_info()

# 双字查询函数，对于双字短语，通过直接查询双字索引返回结果
# param：sentence 短语文本
# return：返回文本编号列表
# date：2019.11.2
def dw_query(sentence):
    return double_index[sentence]

# 作者查询函数，通过直接查询作者索引表放回结果（诗文编号列表）
# param：sentence 短语文本
# return：返回文本编号列表
# date：2019.11.2
def author_query(sentence):
    return author_index[sentence]

# 处理非双字的短语或单字查询，标题的查询函数融入到此函数中
# param：Word_list 单字列表，这里面没有去除“，”和“。”
# param: pos_index 位置索引，可以是标题的位置索引也可以是诗文的位置索引
# return ： 返回一个编号列表，如果没有找到，返回空的数据结构
# date：2019.11.2
def phrase_query(word_list,pos_index):
    res_index = []         # 保存返回结果的编号列表
    pre_dict = dict()              # 保留前一个字的位置信息
    gap = 1
    for i in  range(len(word_list)):
        if word_list[i] in ['，','。']:  # 如果为逗号或者句号，不做处理
            gap = gap+1
            continue
        elif i==0 :
            pre_dict = dict(pos_index[word_list[0]])  # 获取第一个字的位置信息
            res_index.extend(pre_dict.keys())
            continue

        cur_dict = dict(pos_index[word_list[i]])        # 获取该字对应的词项字典
        res_index = [x for x in res_index if x in cur_dict.keys()]
        temp_index = []
        for item in res_index:
            tt = [ i for i in pre_dict[item] if i+gap in cur_dict[item]]
            if len(tt) != 0:
                temp_index.append(item)
        res_index = temp_index
        pre_dict = cur_dict
        gap =1
    return res_index


# 查询函数，传入参数为查询文本
# 函数实现功能为对输入的查询文本进行判断，如果是双字查询则使用双字索引
# 否则，使用位置索引实现基于短语的查询功能，具体的双字查询和短语查询均通过独立的函数实现
# 本函数中只进行调用和相关的处理
# param： query_sentence 查询文本
# return： 结果文本的编号列表
# date：2019.11.2
def query(query_sentence):
    # 定义查询结果变量，存储结果编号列表
    query_result =[]
    # 处理查询文本,判断是否为双字查询，短语查询忽略“，”和“。”
    text_list = [i for i in query_sentence]
    if('，'not in text_list and '。'not in text_list\
            and len(text_list)==2 ):
        query_result = dw_query(query_sentence)                                     # 调用处理双字查询的函数
    else:
        query_result = phrase_query(text_list,title_index)                           # 调用基于位置查询的处理函数查询诗文正文
    # 返回查询结果，如果没有找到，则返回空列表
    return query_result


# 将诗文编号转换为响应的诗文列表,可以对此函数进行修改实现对于返回结果的控制
# param: index_list 诗文编号
# return ： 返回一个诗文信息的列表
def convert_result(index_list):
    return [poets_info[int(i)] for i in index_list]

# 测试调用
index_list = query("山居诗")
print("result_list",len(index_list),index_list)
print(convert_result(index_list))