import os

mail_path = '../enron_mail_20150507/maildir'
target_path = '../enron_mail_dir'

def transfer_files(path_from,path_to):
    files = os.listdir(path_from)
    for file in files:
        if  not os.path.isdir(file) :
            path_temp = path_from+'\\'+file
            print(path_temp)


transfer_files(mail_path)