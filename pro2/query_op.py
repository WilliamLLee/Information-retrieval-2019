# date: 2019年11月1日
# author: lw
# e-mail: lio6218@163.com
# description: 本文件主要实现基于位置索引和双字索引的诗文查询函数，返回匹配的结果

from  data_import_process import import_d_index  # 引入双字索引导入函数
from data_import_process import import_p_index # 引入位置所引导入函数
# from data_import_process import import_poets
from data_import_process import import_author_title_index
from data_import_process import import_poets_info
import re

# 定义查询种类
query_type = {"title":1,"author":2,"paragraphs":3, "mix":4}

# 导入索引和诗文信息内容，进行系统查询内容的构建工作
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
    if sentence in double_index.keys():
        return double_index[sentence]
    else:
        return []
# 作者查询函数，通过直接查询作者索引表放回结果（诗文编号列表）
# param：sentence 短语文本
# return：返回文本编号列表
# date：2019.11.2
def author_query(sentence):
    if sentence in author_index.keys():
        return author_index[sentence]
    else:
        return []

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
    return [int(item) for item in res_index]               # 由于位置索引的文档编号为字符，需要转为int类型的列表

# 支持文本域的与或非查询
def extend_query(query_sentence):
    query_items = re.findall(r"\(|\)|[Aa][Nn][Dd]|[Oo][Rr]|[Nn][Oo][Tt]|[^a-zA-z\(\) ]*",
                             query_sentence)  # 通过正则表达式进行分划区块
    query_items_postfix = convert2postfixexpr(query_items)  # 转为后缀形式的查询
    result = []
    print(query_items_postfix)
    for item in query_items_postfix:
        print(result)
        if re.fullmatch(r"[Aa][Nn][Dd]", item):  # 将result的最上面两个结果合并
            second = result.pop()
            first = result.pop()
            print("and")
            print([i for i in first if i in second])
            result.append(list(set(first).intersection(set(second))))
        elif re.fullmatch(r"[Oo][Rr]", item):  # 或，合并后去重
            second = result.pop()
            first = result.pop()
            print("or")
            result.append(list(set(first).union(set(second))))
        elif re.fullmatch(r"[Nn][Oo][Tt]", item):  # not ,通过count求出对于全局的补集，不能直接求全局的补集，这样代价太大，需要优化一下
            first = result.pop()
            print("not")
            result.append(list(set(range(count)).difference(set(first))))
        else:  # 对查询项进行查询操作，结果压入result
            text_list = [i for i in item]
            print(text_list)
            if ('，' not in text_list and '。' not in text_list \
                    and len(text_list) == 2):  # 调用处理双字查询的函数
                result.append(dw_query(item))
                print(result)
            else:
                result.append(phrase_query(text_list, position_index))  # 调用基于位置查询的处理函数查询诗文正文
                print(result)
    if len(result) == 1:
        return result.pop()
    else:
        return []


# 查询函数，传入参数为查询文本
# 函数实现功能为对输入的查询文本进行判断，如果是双字查询则使用双字索引
# 否则，使用位置索引实现基于短语的查询功能，具体的双字查询和短语查询均通过独立的函数实现
# 本函数中只进行调用和相关的处理
# 默认为混合查询模式，即自行进行判断查询获取结果，较慢，如果需要精准的快速查询选择相应类别的直接查询模块
# param： query_sentence 查询文本
# return： 结果文本的编号列表
# date：2019.11.2
def query(query_sentence,type):
    # 处理查询文本,将查询文本分为一个单字的列表，短语查询忽略“，”和“。”
    if query_type[type] == 1:                   # 标题查询
        text_list = [i for i in query_sentence]
        return phrase_query(text_list,title_index)
    elif query_type[type] == 2:                    # 调用作者查询模块
        return  author_query(query_sentence)
    elif query_type[type] == 3:                     # 诗文文本查询模块，实现与或非的查询功能
        return extend_query(query_sentence)
    elif query_type[type] == 4:                     # 混合查询模式，即不指定特定的查询域，进行所有结果的查询，找到了所有的结果进行合并返回
        text_list = [i for i in query_sentence]
        return []
    # 返回查询结果，如果没有找到，则返回空列表
    return []


# 将获取的与或非表达式item列表转为后缀形式，之后进行与或非查询
# not 优先级最高，and 次之 ， or最低
# param：expr_list 为经过正则处理之后形成的列表
# 返回一个list（栈类型），其中保存一个后缀形式的查询表达式
# date：2019.11.6
def convert2postfixexpr(expr_list):
    sym_stack  = list()          # 符号栈
    item_stack = list()          # 查询元素栈
    queue_dict = {")":4,"not":3,"and":2,"or":1,"(":0} # 定义与或非的优先级
    for item in expr_list :
        if re.fullmatch(r"\(|\)|[Aa][Nn][Dd]|[Oo][Rr]|[Nn][Oo][Tt]",item):   # 匹配运算符
            while(len(sym_stack)!=0):        # 栈不为空，不停弹出栈顶进行比较
                top = sym_stack.pop()          # stack top
                if queue_dict[item.lower()] <= queue_dict[top.lower()]:
                    if top != ')':  # 非），弹出栈顶即可
                        item_stack.append(top)
                        continue
                    else:  # 如果栈顶为”）“,则将括号以内的符号全部弹出
                        while (len(sym_stack) != 0):
                            t_top = sym_stack.pop()
                            if t_top == '(':
                                break
                            item_stack.append(t_top)
                else:           # 优先级更高，入栈退出循环
                    sym_stack.append(top)
                    sym_stack.append(item)
                    break
            if len(sym_stack) == 0:  # empty , push stack
                sym_stack.append(item)
        elif item != "":
            item_stack.append(item)                 # 为查询项则直接入栈
    # 最后如果符号栈不为空，则将符号栈中所有非括号内容全部放入item_stack
    while(len(sym_stack)!=0):
        top  = sym_stack.pop()
        if top not in ["(",")"]:
            item_stack.append(top)
    # 返回后缀形式的查询列表
    return item_stack


# 将诗文编号转换为响应的诗文列表,可以对此函数进行修改实现对于返回结果的控制
# param: index_list 诗文编号
# return ： 返回一个诗文信息的列表
def convert_result(index_list):
    if len(index_list)==0 :
        return []
    return [poets_info[int(i)] for i in index_list]


# 将诗文编号转换为响应的诗文列表,可以对此函数进行修改实现对于返回结果的控制
# 在查询得到的词汇上进行加粗处理,为前端显示做工作
# param: index_list 诗文编号
# return ： 返回一个诗文信息的列表
def convert_result_for_html(index_list,query_sentence,type):
    result = []
    if len(index_list)==0 :
        return result
    else:
        items = re.findall(r"[^a-zA-z\(\) ]*", query_sentence)
        items = [i for i in  items if i != ""]
        for i in  range(len(poets_info)):
            if i in index_list:
                temp = dict(poets_info[i])
                for item in  items:             # 替换加粗显示
                    if str(temp[type]).find(item) != -1:
                        temp[type] = str(temp[type]).replace(item,"<b>"+item+"</b>")
                result.append(temp)
    return result

# # 测试调用
# index_list = query("李白","title")
# print("result_list",len(index_list),index_list)
# print(convert_result(index_list))