from inverted_index_build import *


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
        score[file] = score[file]/words_count_of_file[file][1]

    rank_list = sorted(score.items(),key=lambda x:x[1],reverse=True)
    print(rank_list)

test_sentence = 'aod@newsdata.com'
querry(test_sentence,index_dict,words_count_of_file,'-F')

