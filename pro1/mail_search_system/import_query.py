from  pre_index_build  import *

# 导入索引的具体函数，从files_path文件中获取最新的检索列表存储路径
def import_index(files_path):
    f = open(files_path,'r',encoding='utf-8')
    path = []
    for line in f :
        path.append(line.strip('\n'))
    info_path = path[0]
    index_path = path[1]
    print(info_path,index_path)

    index_dict = {}
    words_count_of_file = {}

    infof  = open(info_path,'r',encoding='utf-8')
    for line in infof:
        info_list = line.strip('\n').split(',')
        words_count_of_file[info_list[0]] = [0 for i in range(len(order.keys()) + 1)]
        for i in range(len(order.keys()) + 1):
            if i == 0 :
                words_count_of_file[info_list[0]][i] = int(info_list[i+1])
                continue
            words_count_of_file[info_list[0]][i] = float(info_list[i+1])
    infof.close()

    indexf = open(index_path, 'r', encoding='utf-8')
    for line in indexf:
        index_list = line.strip('\n').split('#')
        index_dict[index_list[0]] = {}
        for i in range(len(index_list)):
            if i == 0:
                continue
            cc = index_list[i].split(':')
            index_dict[index_list[0]][cc[0]] = float(cc[1])
    indexf.close()

    return words_count_of_file,index_dict

# 获取键盘输入，进行查询匹配，返回排序后的检索评分结果

def  query(q_sentence,index_dict,words_count_of_file,type):
    length,count = split_lemmatize(q_sentence,type)
    score = {}
    file_count_num = len(words_count_of_file.keys())  # 文件数

    for file in words_count_of_file.keys():
        score[file] = 0.0
        for item in count.keys():
            if item+type not in index_dict.keys():
                continue
            if file in index_dict[item+type].keys():
                w = index_dict[item+type][file]
            else :
                w = 0
            temp = (1+math.log(count[item]))*math.log(file_count_num/len(index_dict[item+type].keys()))*w
            score[file] = score[file] +temp
        a_len = words_count_of_file[file][order[type[-1]]]
        if a_len == 0 :
            score[file] = 0.0
            continue
        score[file] = score[file]/a_len

    rank_list = sorted(score.items(),key=lambda x:x[1],reverse=True)
    return rank_list


