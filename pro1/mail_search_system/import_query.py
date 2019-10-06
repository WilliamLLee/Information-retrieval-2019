from  pre_index_build  import *

def import_index(files_path):
    f = open(files_path,'r',encoding='utf-8')
    path = []
    for line in f :
        path.append(line.strip('\n'))
    info_path = path[0]
    index_path = path[1]
    print(info_path,index_path)
    info = {}
    with codecs.open(info_path , "r", "utf-8") as f:
        for line in f:
            info = json.loads(line)
    print ('=> info of files import succeed!')

    index = {}
    with codecs.open(index_path , "r", "utf-8") as f:
        for line in f:
            index = json.loads(line)
    print('=> index import succeed!')

    return info ,index

# 获取键盘输入，进行查询匹配

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

# test = 'Tue, 12 Dec 2000 23:04:00 -0800 (PST)'
info_dict,index_dict = import_index(files)
# print(query(test,index_dict,info_dict,'-D'))