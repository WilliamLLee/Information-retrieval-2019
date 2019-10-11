import os
import nltk
from collections import Counter
from nltk.stem import *
import math
import time
import re


mail_path = '..\enron_mail_20150507\maildir'  #邮件文件根目录
number_file = '.\mail_list.txt'        # 存储文件编号映射表
split_word_error = '.\splits_error.txt'   # 存储分词过程中的error信息
target_path = './index_files'       # 索引文件保存目标路径


#对数据集中的所有文件进行编号，将其文件目录输出到一个文件中
#path:邮件的存储文件夹
#number_file:为存储邮件编号列表的txt文件路径
#控制台输出的count变量数据显示处理的文件数量
def list_files(path,number_file):
    f = open(number_file,'w',encoding='utf-8')
    # 遍历根目录
    count = 1
    for root,dirs,files in os.walk(path,topdown=True):
        for file in files :
            path_t = os.path.join(root,file)
            f.write(str(count)+':'+path_t+'\n')
            count=count+1
            print(count)
    f.close()


# 分词&词形还原函数
# sentence 为输入的单词串
# 此函数采用yield 实现迭代器，返回一个单词的迭代器
# 返回值为经过词形还原之后的一个一个的单词或符号
def lemmatize_all(sentence):
    wnl = WordNetLemmatizer()     # 声明一个词形还原器
    for word, tag in nltk.pos_tag(re.findall(r'[0-9]+[:][0-9]+[:][0-9]+|[0-9]+[:][0-9]+|[0-9]+[.][0-9]+|[0-9]+|[A-Za-z]+[-\'][A-Za-z]+|[A-Za-z]+|[@$]+',sentence)):  # 先正则分词，再给不同的词贴上标签
        if tag.startswith('NN'):    # 根据标注的不同词性对单词进行词形还原
            yield wnl.lemmatize(word, pos='n')
        elif tag.startswith('VB'):
            yield wnl.lemmatize(word, pos='v')
        elif tag.startswith('JJ'):
            yield wnl.lemmatize(word, pos='a')
        elif tag.startswith('R'):
            yield wnl.lemmatize(word, pos='r')
        else:
            yield word

#输出句子分词之后的词项和词频，并统计句子的单词总数
#调用lemmatize_all(分词) 函数，并将返回的词条迭代器转换为一个单词列表
#通过使用counter函数，将单词列表进行词项统计工作，返回一个字典
#此函数另一个返回值为该输入字符串分词后的单词总数
def split_lemmatize(sentence,type):
    # 全部转换为小写字符
    sentence_proc = sentence.lower()
    # nltk分词以及词形还原
    words = []
    if type == '-C' or type == '-S':
        words =[i for i in lemmatize_all(sentence_proc) ]       # 基于nltk分词，将结果以列表形式存储
    elif type == '-D':
        words = re.findall(r'[0-9]+[:][0-9]+[:][0-9]+|[0-9]+|[A-Za-z]+',sentence_proc)
    elif type == '-F' or type == '-T':
        words = re.findall(r'[0-9]+[.][0-9]+|[0-9]+|[A-Za-z]+|[@]+',sentence_proc)
    # print(sentence)
    # print(words)
    count = Counter(words)       # 使用counter进行计数，counter继承了Python的字典数据结构能够很好的解决索引问题
    return len(words),count      #返回句子分词和词形还原之后统计的词条总数以及词项频数



# 直接从文件列表中读入文件路径
# 打开文件，读取不同域的文本进行分词建立一个倒排索引表
# 索引表中存放的信息包括 词项字典，词项由两分部分组成，即词项以及域后缀，同时在后面通过一个数字计算该词项在多少个文档中出现
# 之后跟随在词项后的为一个列表，每一项为文件编号和在该文件中该词项出现的次数

# 给不同域的词项后缀进行标号,用于为不同的文本域进行存储向量空间长度做标志
order = {'D':1,'F':2,'T':3,'S':4,'C':5}

files = './file_content.txt'           # 保存最新的两个文件，querry始终读取这两个文件路径

def index_build(mail_list_file,target_path,files_path):
    f_read = open(mail_list_file,'r',encoding='utf-8')  #打开文件映射表
    file_list = []          # 将文件映射表内容存在这个2*x维列表中
    for line in f_read :
        mail = line.strip('\n').split(":")
        file_list.append(mail)
    f_read.close()

    # 记录词项倒排索引表
    file_count_num = len(file_list)     # 文件的总数
    print('=>文件总数为：',file_count_num)
    index_dict = {}
    words_count_of_file ={}

    # 记录所有的文本域
    title_list = ['Message-ID','Date','From','To','Subject','Cc','Mime-Version','Content-Type','Content-Transfer-Encoding','Bcc','X-From','X-To','X-cc','X-bcc','X-Folder','X-Origin','X-FileName']
    for file in file_list:          #开始对每一个文件进行分词，并同时将信息输出到文件中
        word_dict = {}    # 存储不同域的单词串，进行域的划分
        try :
            content = open(file[1], 'r', encoding='utf-8')  # 打开一个文件进行读取
            former_word = ''                    # 提示前一行的文本域名，对分域操作进行辅助，因存在一个文本域分布于多行的特殊情况
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
            f1 = open(split_word_error,'a',encoding='utf-8')  #输出错误信息到error文件
            f1.write('ERROR : '+file[0]+': '+file[1]+'\n')
            f1.close()
            print("ERROR:"+file[0])   #控制台输出错误信息提示
        else :
            print(file[0])  # 显示当前进度
            # # 开始将文件处理的结果写入分词结果文本中去
            for item in ['Date', 'From', 'To', 'Subject', 'Content']:   # 筛选目的文本域进行分词处理
                if item in word_dict.keys():
                    length, count = split_lemmatize(word_dict[item],'-'+item[0])        # 判断文本域，并根据文本域调用相应分词函数
                    words_count_of_file[file[0]] = [0 for i in range(len(order.keys())+1)]         # 记录文件的单词数量以及该文件不同域的向量空间的长度平方值，设置好列表的大小
                    words_count_of_file[file[0]][0] = length        # 记录该文件单词数数量
                    for temp in count.keys():
                        key = temp+'-'+item[0]              # 给单词加上文本域后缀
                        if key not in index_dict.keys():            # 单词不存在现有的词项字典中，则创建字典词项对应的字典的项
                            file_dict={file[0]:count[temp]}
                            index_dict[ key] = file_dict
                        else:                                       # 否则在现有的字典词项对应的文件索引字典中创建相应的项添加上
                            index_dict[ key][file[0]]= count[temp]


        # if int(file[0]) > 1000 :
        #     break
    print('=>index building end successfully!')           # 索引建立完毕提示


    #  构建索引并保存索引的相关代码，下面是相关提示信息输出
    index_path =  target_path+'/'+time.strftime('%Y-%m-%d',time.localtime(time.time()))+ '_index.txt'
    file_info_path =  target_path+'/'+time.strftime('%Y-%m-%d',time.localtime(time.time()))+ '_file_info.txt'
    print ('=>save index to file :'+index_path+'\n=>save information of files to :'+ file_info_path )

    indexf = open(index_path, 'w', encoding='utf-8')  # 打开索引输出文件流
    infof = open(file_info_path, 'w', encoding='utf-8')  # 打开文件输出流，输出文件中不同域文本的向量空间长度
    for item in index_dict.keys():
        df = len(index_dict[item])
        indexf.write(item)
        for temp in index_dict[item].keys():
            index_dict[item][temp] = math.log(file_count_num / df) * (1 + math.log(index_dict[item][temp]))
            words_count_of_file[temp][order[item[-1]]] = words_count_of_file[temp][order[item[-1]]] +math.pow(index_dict[item][temp] ,2)
            indexf.write( format('#'+temp+':%.2f'%index_dict[item][temp]))
        indexf.write('\n')
    for item in words_count_of_file:
        infof.write(item)
        for temp in  range(len(words_count_of_file[item])):
            if temp != 0:
                infof.write( format(',%.4f'%math.sqrt(words_count_of_file[item][temp])))
            else :
                infof.write(','+str(words_count_of_file[item][temp]))
        infof.write('\n')
    infof.close()
    indexf.close()
    print('=>index table save successfully！')

    f = open(files, 'w', encoding='utf-8')
    f.write(file_info_path + '\n')
    f.write(index_path + '\n')
    f.close()

    return 'SUCCEED!'

# 建索引，存储
# index_build(number_file, target_path, files)
