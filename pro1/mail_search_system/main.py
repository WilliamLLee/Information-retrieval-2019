# -*- coding: utf-8 -*-
from flask import Flask, jsonify, render_template,request
from flask_cors import  *
from  query import *
from get_audio import *
from speech_recognition import *

app = Flask(__name__)  # 实例化app对象
CORS(app,supports_credentials=True)    # 解决跨域请求无响应问题


def tran_json(res):
    f_read = open('..\mail_list.txt','r',encoding='utf-8')  #打开文件映射表
    file_list = {}          # 将文件映射表内容存在这个2*x维列表中
    for line in f_read :
        mail = line.strip('\n').split(":")
        file_list[mail[0]] = mail[1]
    f_read.close()

    res_j = []
    for item in  res:
        res_j.append(
            {
                'path': file_list[item[0]],
                'score': item[1]
            }
        )
    return  jsonify(res_j)


@app.route('/',methods=['GET','POST'])
def query():
    print(request.form)
    test_sentence = request.form['sentence']
    type_s = request.form['type_s']
    result = querry(test_sentence, index_dict, words_count_of_file, type_s)
    print( tran_json(result))
    return tran_json(result)

@app.route('/recording',methods=['GET','POST'])
def recoding():
    return get_audio(in_path)

@app.route('/audio',methods=['GET','POST'])
def audioQuery():
    signal = open(in_path, "rb").read()
    rate = 16000
    token = get_token()
    test_sentence = recognize(signal, rate, token)['result'][0]
    print(test_sentence)
    type_s = request.form['type_s']
    result = querry(test_sentence, index_dict, words_count_of_file, type_s)
    print( tran_json(result))
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)



