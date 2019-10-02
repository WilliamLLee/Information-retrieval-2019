from file_pretreatment import *
import math
import time

# 直接从文件列表中读入文件路径
# 打开文件，读取不同域的文本进行分词建立一个倒排索引表
# 索引表中存放的信息包括 词项字典，词项由两分部分组成，即词项以及域后缀，同时在后面通过一个数字计算该词项在多少个文档中出现
# 之后跟随在词项后的为一个列表，每一项为文件编号和在该文件中该词项出现的次数

# 给不同域的词项后缀进行标号
order = {'D':1,'F':2,'T':3,'S':4,'C':5}

files = './files_content.txt'           # 保存最新的两个文件，querry始终读取这两个文件路径

def index_build(mail_list_file,target_path):
    f_read = open(mail_list_file,'r',encoding='utf-8')  #打开文件映射表
    file_list = []          # 将文件映射表内容存在这个2*x维列表中
    for line in f_read :
        mail = line.strip('\n').split(":")
        file_list.append(mail)
    f_read.close()
    # 记录词项倒排索引表
    index_dict = {}
    words_count_of_file ={}
    # 记录所有的文本域
    title_list = ['Message-ID','Date','From','To','Subject','Cc','Mime-Version','Content-Type','Content-Transfer-Encoding','Bcc','X-From','X-To','X-cc','X-bcc','X-Folder','X-Origin','X-FileName']
    for file in file_list:          #开始对每一个文件进行分词，并同时将信息输出到文件中
        word_dict = {}    # 存储不同域的单词串，进行域的划分
        try :
            content = open(file[1], 'r', encoding='utf-8')  # 打开一个文件进行读取
            former_word = ''
            for line in content:
                top_word = line.split(':')[0]
                if top_word == 'X-FileName':
                    word_dict['Content'] = ''
                if top_word in title_list and former_word != 'X-FileName':
                    word_dict[top_word] = line.strip(top_word + ':').strip('\n').strip('\t')
                    former_word = top_word
                    continue
                elif former_word == 'X-FileName':
                    word_dict['Content'] = word_dict['Content'] + ' ' + line.strip('\n').strip('\t')
                    continue
                else:
                    word_dict[former_word] = word_dict[former_word] + ' ' + line.strip('\n').strip('\t')
            content.close()  # 关闭读取文件流

        except UnicodeDecodeError:
            f1 = open(split_word_error,'a',encoding='utf-8')
            f1.write('ERROR : '+file[0]+': '+file[1]+'\n')
            f1.close()
            print("ERROR:"+file[0])
        else :
            print(file[0])  # 显示当前进度
            # # 开始将文件处理的结果写入分词结果文本中去
            for item in ['Date', 'From', 'To', 'Subject', 'Content']:   # 筛选目的文本域进行分词处理
                if item in word_dict.keys():
                    length, count = split_lemmatize(word_dict[item])
                    # print(count,word_dict[item])
                    words_count_of_file[file[0]] = [0 for i in range(len(order.keys())+1)]         # 记录文件的单词数量以及该文件不同域的向量空间的长度平方值
                    words_count_of_file[file[0]][0] = length        # 记录单词数数量
                    for temp in count.keys():
                        key = temp+'-'+item[0]
                        if key not in index_dict.keys():
                            file_dict={file[0]:count[temp]}
                            index_dict[ key] = file_dict
                        else:
                            index_dict[ key][file[0]]= count[temp]


        if int(file[0]) > 1000 :
            break
    # print(index_dict)
    length1 = (index_dict.keys().__len__())
    print(length1)
    print('=>index building end successfully!')           # 索引建立完毕提示


    #  索引保存代码
    index_path =  target_path+'/'+time.strftime('%Y-%m-%d',time.localtime(time.time()))+ '_index.txt'
    file_info_path =  target_path+'/'+time.strftime('%Y-%m-%d',time.localtime(time.time()))+ '_file_info.txt'
    print ('=>save index to file :'+index_path+'\n=>save information of files to :'+ file_info_path )
    indexf = open(index_path,'w',encoding='utf-8')     # 打开索引输出文件流
    infof = open(file_info_path, 'w', encoding='utf-8')     # 打开文件输出流，输出文件中不同域文本的向量空间长度

    for item in index_dict.keys():
        df = len(index_dict[item])
        indexf.write(item)
        for temp in index_dict[item].keys():
            index_dict[item][temp] = math.log(1000 / df) * (1 + math.log(index_dict[item][temp]))
            words_count_of_file[temp][order[item[-1]]] = words_count_of_file[temp][order[item[-1]]] +math.pow(index_dict[item][temp] ,2)
            indexf.write('#'+temp+':'+str(index_dict[item][temp]))
        indexf.write('\n')
    for item in words_count_of_file:
        infof.write(item)
        for temp in  range(len(words_count_of_file[item])):
            infof.write(','+str(words_count_of_file[item][temp]))
        infof.write('\n')
    infof.close()
    indexf.close()
    print('=>index table save successfully！')
    #print(words_count_of_file)
    # return  index_dict,words_count_of_file,file_info_path,index_path
    return file_info_path, index_path


# index_dict,words_count_of_file,info_file,index_file= index_build(number_file ,'./index_files')


# info_file,index_file= index_build(number_file ,'./index_files')
# f = open(files,'w',encoding='utf-8')
# f.write(info_file+'\n')
# f.write(index_file+'\n')
# f.close()