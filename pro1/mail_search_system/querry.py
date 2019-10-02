from inverted_index_build import *


# 从文件中获取索引信息
def get_index(files):
    f = open(files,'r',encoding='utf-8')
    index_file = ''
    info_file = ''
    for line in f :
        if info_file == '':
            info_file = line.strip('\n')
            continue
        if index_file =='':
            index_file = line.strip('\n')
            continue

    indexf = open(index_file,'r',encoding='utf-8')
    infof  = open(info_file,'r',encoding='utf-8')

    index_dict = {}
    words_count_of_file ={}
    for line in infof:
        info_list = line.strip('\n').split(',')
        words_count_of_file[info_list[0]] = [0 for i in range(len(order.keys()) + 1)]
        for i in range(len(order.keys()) + 1):
            if i == 0 :
                words_count_of_file[info_list[0]][i] = int(info_list[i+1])
                continue
            words_count_of_file[info_list[0]][i] = float(info_list[i+1])

    for line in indexf :
        index_list = line.strip('\n').split('#')
        index_dict[index_list[0]] = {}
        for i in range (len(index_list)):
            if i == 0 :
                continue
            cc = index_list[i].split(':')
            index_dict[index_list[0]][cc[0]] = float(cc[1])
    indexf.close()
    infof.close()

    return index_dict,words_count_of_file


# 获取键盘输入，进行查询匹配

def querry(q_sentence,index_dict,words_count_of_file,type):
    length,count = split_lemmatize(q_sentence)
    score = {}
    for file in words_count_of_file.keys():
        score[file] = 0.0
        for item in count.keys():
            if item+type not in index_dict.keys():
                continue
            if file in index_dict[item+type].keys():
                w = index_dict[item+type][file]
            else :
                w = 0
            temp = (1+math.log(count[item]))*math.log(1000/len(index_dict[item+type].keys()))*w
            score[file] = score[file] +temp
        a_len = words_count_of_file[file][order[type[-1]]]
        if a_len == 0 :
            score[file] = 0.0
            continue
        score[file] = score[file]/a_len

    rank_list = sorted(score.items(),key=lambda x:x[1],reverse=True)
    print(rank_list)

test_sentence = 'Please use the second check as the October payment.'
index_dict,words_count_of_file = get_index(files)
print ( '=> index import succeeded!')
querry(test_sentence,index_dict,words_count_of_file,'-C')


