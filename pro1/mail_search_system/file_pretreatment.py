import os
import shutil  # 拷贝文件
import nltk

mail_path = '..\enron_mail_20150507\maildir'
#target_path = '..\enron_mail_dir'
number_file = '..\mail_list.txt'
target_file = '..\splits_words_file'

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


#输出句子分词之后的词项和词频，并统计句子的单词总数
def split(sentence):
    count_dict={} #存储单词的词项信息,字典的数据结构
    words = nltk.word_tokenize(sentence.lower())

    print(words)


#按照不同的行，将文本进行分词、正规化，统计每个词的数量，
#将结果输出到文件中，每5万封邮件信息输出到一个文件中，注意处理过程中的报错输出到error.txt文件
def split_words(mail_list_file,target_path,limit_number):
    f_read = open(mail_list_file,'r',encoding='utf-8')
    file_list = []
    for line in f_read :
        mail = line.strip('\n').split(":")
        file_list.append(mail)
    for file in file_list:
        content = open (file[1],'r',encoding='utf-8')
        for line in content:
            sentence = line.split(':')
            print(sentence)
        print(file[0])



# ['Message-ID', ' <25151037.1075855695507.JavaMail.evans@thyme>\n']
# ['Date', ' Thu, 29 Mar 2001 04', '01', '00 -0800 (PST)\n']
# ['From', ' phillip.allen@enron.com\n']
# ['To', ' jacquestc@aol.com\n']
# ['Subject', ' Re', '\n']
# ['Mime-Version', ' 1.0\n']
# ['Content-Type', ' text/plain; charset=us-ascii\n']
# ['Content-Transfer-Encoding', ' 7bit\n']
# ['X-From', ' Phillip K Allen\n']
# ['X-To', ' JacquesTC@aol.com @ ENRON\n']
# ['X-cc', ' \n']
# ['X-bcc', ' \n']
# ['X-Folder', ' \\Phillip_Allen_June2001\\Notes Folders\\All documents\n']
# ['X-Origin', ' Allen-P\n']
# ['X-FileName', ' pallen.nsf\n']
# ['\n']
# ['Jacques\n']
# ['\n']
# ['I am out of the office for the rest of the week.  Have you ever seen anyone \n']
# ['miss as much work as I have in the last 6 weeks?  I assure you this is \n']
# ['unusual for me.\n']
# ['Hopefully we can sign some documents on Monday.  Call me on my cell phone if \n']
# ['you need me.\n']
# ['\n']
# ['Phillip']

str =' Thu, 29 Mar 2001 04 01 00 -0800 (PST)\n'
split(str)
#为文件进行编号处理
#list_files(mail_path,number_file)
# split_words(number_file,target_file,100)
