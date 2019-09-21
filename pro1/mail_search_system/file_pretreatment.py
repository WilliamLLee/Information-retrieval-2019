import os
import shutil  # 拷贝文件


mail_path = '..\enron_mail_20150507\maildir'
#target_path = '..\enron_mail_dir'
number_file = '..\mail_list.txt'

#将数据集中的文本集中到一个文件中，同时通过文件目录的相关信息确定文件名
def list_files(path):
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

#对数据集中的所有文件进行编号，将其文件目录输出到一个文件中
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


#从集中的文本数据目录下读取文本进行分词，返回的数据结果为一个单词字典，确定不同单词在某一个文本中出现的次数
#def split_words(mail_list,):

# 先小范围利用分词分别取内容，主题，收发件人信息，分别进行存储，采用字典的数据结构
# 在大范围使用的时候，采取分段输出的方式，减轻内存压力
# 对于四种不同的检索模式，分别在后面添加不同的后缀作为区别，比如-c\-su\-r\-se进行区分
# 收集的数据包括不同位置此项在文本中的出现次数以及在多少个文本出现，同时记录文本中单词的数量


list_files(mail_path)