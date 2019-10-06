# -*- coding: utf-8 -*-
from flask import Flask, jsonify, render_template,request
from flask_cors import  *
from import_query import *
from get_audio import *
from speech_recognition import *

app = Flask(__name__)  # 实例化app对象
CORS(app,supports_credentials=True)    # 解决跨域请求无响应问题


def tran_result(res):
    f_read = open('..\mail_list.txt','r',encoding='utf-8')  #打开文件映射表
    file_list = {}          # 将文件映射表内容存在这个2*x维列表中
    for line in f_read :
        mail = line.strip('\n').split(":")
        file_list[mail[0]] = mail[1]
    f_read.close()

    res_j = []
    for item in  res:
        if item[1]>0:           # 结果只输出评分不为0的
            res_j.append(
                {
                    'path': file_list[item[0]],
                    'score': item[1]
                }
            )

    return  res_j


@app.route('/',methods=['GET','POST'])
def query_text():
    # print(request.form)
    test_sentence = request.form['sentence']
    type_s = request.form['type_s']
    result = query(test_sentence,index_dict,info_dict,type_s)
    # print( tran_result(result))
    return jsonify(tran_result(result))



@app.route('/audio',methods=['GET','POST'])
def audioQuery():
    get_audio(in_path)
    signal = open(in_path, "rb").read()
    rate = 16000
    token = get_token()
    rec = recognize(signal, rate, token)
    if 'result' in rec.keys():
        test_sentence = rec['result'][0]
    else:
        return json.dumps({"error": 'no input'}), 500
    print(test_sentence)
    type_s = request.form['type_s']
    result = query(test_sentence,index_dict,info_dict,type_s)
    # print( tran_result(result))
    return  jsonify({'sentence':test_sentence,'result':tran_result(result)})

@app.route('/text',methods=['GET','POST'])
def readText():
    path = request.form['path']
    f = open(path,'r',encoding='utf-8')
    str = ''
    for line in f :
        str = str+line
    return str


if __name__ == '__main__':
    app.run(debug=True)



