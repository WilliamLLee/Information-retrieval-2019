import os
import shutil  # 拷贝文件
import nltk
from collections import Counter
from nltk.stem import *


mail_path = '..\enron_mail_20150507\maildir'  #邮件文件根目录
#target_path = '..\enron_mail_dir'
number_file = '..\mail_list.txt'        # 存储文件编号映射表
word_info_file = '.\splits_words_info.txt'   #存储每一个文件的相应域的分词信息
split_word_error = '.\splits_error.txt'   # 存储分词过程中的error信息
split_log = '.\split_log.txt'  #日志文件

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

#将数据集中的文本集中到一个文件中，同时通过文件目录的相关信息确定文件名
# def transfer_files(path_from,path_to):
#     # 遍历根目录
#     for root,dirs,files in os.walk(path_from,topdown=True):
#         for file in files :
#             path_t = os.path.join(root,file)
#             temp = path_t.split('\\')
#             new_file = ''
#             if temp[-3] == 'maildir':
#                 new_file = target_path+'\\'+temp[-2]+'-'+temp[-1]
#             else:
#                 new_file = target_path + '\\' +temp[-3]+'-'+ temp[-2] + '-' + temp[-1]
#             shutil.copyfile(path_t,new_file)

#处理计划
#从文件中的文本数据目录下读取文本进行分词，返回的数据结果为一个单词字典，确定不同单词在某一个文本中出现的次数
# 先小范围利用分词分别取内容，主题，收发件人信息，分别进行存储，采用字典的数据结构
# 在大范围使用的时候，采取分段输出的方式，减轻内存压力
# 对于四种不同的检索模式，分别在后面添加不同的后缀作为区别，比如-c\-su\-r\-se进行区分
# 收集的数据包括不同位置此项在文本中的出现次数以及在多少个文本出现，同时记录文本中单词的数量


# 分词&词形还原函数
# sentence 为输入的单词串
# 此函数采用yield 实现迭代器，返回一个单词的迭代器
# 返回值为经过词形还原之后的一个一个的单词或符号
def lemmatize_all(sentence):
    wnl = WordNetLemmatizer()     # 声明一个词形还原器
    for word, tag in nltk.pos_tag(nltk.word_tokenize(sentence)):  # 先分词，再给不同的词贴上标签
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
def split_lemmatize(sentence):
    # 全部转换为小写字符
    sentence_proc = sentence.lower()
    #去除特殊字符
    special_items = ['*','-','_','=','\\','/','#','$','%','^','&','(',')','~','<','>','.',',','@','\'']
    for item in special_items:
        sentence_proc = sentence_proc.replace(item,' ')
    # nltk分词以及词形还原
    words =[i for i in lemmatize_all(sentence_proc) ]       # 基于nltk分词，将结果以列表形式存储
    count = Counter(words)       # 使用counter进行计数，counter继承了Python的字典数据结构能够很好的解决索引问题
    return len(words),count      #返回句子分词和词形还原之后统计的词条总数以及词项频数


#按照不同的行，将文本进行分词、正规化，统计每个词的数量，
#将结果输出到文件中，每5万封邮件信息输出到一个文件中，注意处理过程中的报错输出到error.txt文件
def split_words(mail_list_file,target_path,limit_number):
    f_read = open(mail_list_file,'r',encoding='utf-8')  #打开文件映射表
    file_list = []          # 将文件映射表内容存在这个2*x维列表中
    for line in f_read :
        mail = line.strip('\n').split(":")
        file_list.append(mail)
    f_read.close()

    title_list = ['Message-ID','Date','From','To','Subject','Cc','Mime-Version','Content-Type','Content-Transfer-Encoding','Bcc','X-From','X-To','X-cc','X-bcc','X-Folder','X-Origin','X-FileName']
    f_write = open(target_path,'w',encoding='utf-8')
    f_log = open(split_log,'w',encoding='utf-8')
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
            f_log.write('ERROR : '+file[0] + ' ' + file[1] + '\n')
            print("ERROR:"+file[0])
        else :
            print(file[0])  # 显示当前进度
            # 开始将文件处理的结果写入分词结果文本中去
            f_write.write(file[0] + '@@')

            # 输出处理日志文件
            f_log.write(file[0] + ' ' + file[1] + '\n')
            f_log.write('{ ')
            for item in word_dict.keys():
                f_log.write('"' + item + '"' + ':' + '"' + word_dict[item] + '"')
                f_log.write(' ')
            f_log.write('}\n')
            for item in ['Date', 'From', 'To', 'Subject', 'Content']:
                if item in word_dict.keys():
                    len, count = split_lemmatize(word_dict[item])
                    f_write.write('{ (' + item + ',' + str(len) + ')' + ':::')

                    f_log.write('"' + item + '"' + ' ' + str(len) + ' ')
                    f_log.write('{ ')
                    for temp in count.keys():
                        f_write.write('[' + temp + '::' + str(count[temp]) + ']')
                        f_log.write('"' + temp + '"' + ':' + str(count[temp]))
                        f_log.write(' ')
                    f_log.write("}\n")

                    f_write.write('}')


    f_write.close()
    f_log.close()
    print('end!')


# 343
# ['Message-ID', ' <17864070.1075855695090.JavaMail.evans@thyme>\n']
# ['Date', ' Thu, 12 Apr 2001 03', '09', '00 -0700 (PDT)\n']
# ['From', ' phillip.allen@enron.com\n']
# ['To', ' jeff.richter@enron.com, tim.belden@enron.com, tim.heizenrader@enron.com\n']
# ['Subject', ' \n']
# ['Mime-Version', ' 1.0\n']
# ['Content-Type', ' text/plain; charset=us-ascii\n']
# ['Content-Transfer-Encoding', ' 7bit\n']
# ['X-From', ' Phillip K Allen\n']
# ['X-To', ' Jeff Richter, Tim Belden, Tim Heizenrader\n']
# ['X-cc', ' \n']
# ['X-bcc', ' \n']
# ['X-Folder', ' \\Phillip_Allen_June2001\\Notes Folders\\All documents\n']
# ['X-Origin', ' Allen-P\n']
# ['X-FileName', ' pallen.nsf\n']
# ['\n']
# ["Here is a simplistic spreadsheet.  I didn't drop in the new generation yet, \n"]
# ['but even without the new plants it looks like Q3 is no worse than last year.\n']
# ['Can you take a look and get back to me with the bullish case?\n']
# ['\n']
# ['thanks,\n']
# ['\n']
# # ['Phillip\n']

# 为文件进行编号处理
# list_files(mail_path,number_file)
# 分词，并将分词结果输出到文件中进行存储
# split_words(number_file,word_info_file,100)

