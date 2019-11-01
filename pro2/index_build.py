# date: 2019年10月28日
# author: 李伟
# e-mail: lio6218@163.com
# description: 本文件主要实现对诗文的文本处理，包括分词函数的实现和索引表构建等

from data_import_process import import_poets
import json

# 位置索引存储路径
position_index = "./create/position_index/"
double_index = "./create/double_index/"

# 构建位置索引和双字索引
# 即以单字为词项，其后跟随存在该词项的诗文编号和出现该词项的偏移量
def build_position_index(position_index_file,double_index_file,poets):
    word_index_t = {}
    dword_index_t = {}
    for no in range(len(poets)):
        if(no%1000==0):
            print("->>>>>>",no)
        word_list = [i for i in poets[no]]
        length = len(word_list)
        for i in range(length):
            # 构建双字索引表
            if (i > 0 and word_list[i] not in['，', '。'] and word_list[i-1] not in ['，', '。']):
                word_item = word_list[i-1]+word_list[i]
                #print(word_item)
                if word_item not in dword_index_t.keys():
                    dword_index_t[word_item] = [no]
                else:
                    if (no not in dword_index_t[word_item]):
                        dword_index_t[word_item].append(no)

            # 构建单字索引表
            if word_list[i] in ['，','。']:       # 构建单字索引跳过逗号和句号
                continue
            if(word_list[i] not in word_index_t.keys()):
                word_index_t[word_list[i]] = {  no:[i],}
            else:
                if(no not in word_index_t[word_list[i]].keys()):
                    word_index_t[word_list[i]][no]=[i]
                else:
                    word_index_t[word_list[i]][no].append(i)
    # 把字典转为列表格式，分块存储
    w_list = word_index_t.items()
    d_list = dword_index_t.items()

    temp = []
    count =  0
    for item in w_list:
        temp.append(item)
        if(len(temp)==500):
            dump_s = open(position_index_file + "%d.json" % (count*500), 'w', encoding="UTF-8")
            json.dump(temp, dump_s, indent=0, ensure_ascii=False)
            dump_s.close()
            temp.clear()
            count=count+1
            print("pos<<<<",count)
    dump_d = open(position_index_file + "%d.json" % (count*500), 'w', encoding="UTF-8")
    json.dump(temp, dump_d, indent=0, ensure_ascii=False)
    dump_d.close()

    temp.clear()
    count = 0
    print("---->>>>>单字索引存储完成,有词项",len(w_list))
    for item in d_list:
        temp.append(item)
        if(len(temp)==10000):
            dump_d = open(double_index_file + "%d0000.json" % (count), 'w', encoding="UTF-8")
            json.dump(temp, dump_d, indent=0, ensure_ascii=False)
            dump_d.close()
            temp.clear()
            count=count+1
            print("dou<<<<", count)
    dump_d = open(double_index_file + "%d0000.json" % (count), 'w', encoding="UTF-8")
    json.dump(temp, dump_d, indent=0, ensure_ascii=False)
    dump_d.close()
    print("---->>>>>双字索引存储完成，有词项",len(d_list))
    # print(word_index_t)
    # print(dword_index_t)

# 调试代码
count,poets = import_poets()
build_position_index(position_index,double_index,poets)




