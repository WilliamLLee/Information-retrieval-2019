# date: 2019年11月1日
# author: lw
# e-mail: lio6218@163.com
# description: 本文件主要实现基于位置索引和双字索引的诗文查询函数，返回匹配的结果

from  data_import_process import import_d_index  # 引入双字索引导入函数
from data_import_process import import_p_index # 引入位置所引导入函数

# 导入索引
double_index = import_d_index()
position_index = import_p_index()

# 双字查询函数，对于双字短语，通过直接查询双字索引返回结果
# param：sentence 短语文本
# return：返回文本编号列表
# date：2019.11.2
def dw_query(sentence):
    return double_index[sentence]

# 处理非双字的短语或单字查询
# param：Word_list 单字列表，这里面没有去除“，”和“。”
# return ： 返回一个编号列表
# date：2019.11.2
def phrase_query(word_list):

    return 0


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
    if('，'not in text_list and '。'not in text_list \
            and len(text_list)==2 ):
        query_result = dw_query(query_sentence)                                     # 调用处理双字查询的函数
    else:
        print("处理非双字短语查询或单字查询，基于位置索引")                           # 调用基于位置查询的处理函数
    # 返回查询结果，如果没有找到，则返回空列表
    return query_result


# 测试调用
print(query("瘦马"))