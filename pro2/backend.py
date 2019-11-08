# date: 2019年11月3日
# author: lw
# e-mail: lio6218@163.com
# description: 实现后端的处理返回函数，基于flask包

# -*- coding: utf-8 -*-
from flask import Flask, jsonify, render_template,request
from flask_cors import  *
from query_op import *
import json

app = Flask(__name__)  # 实例化app对象
CORS(app,supports_credentials=True)    # 解决跨域请求无响应问题
# 响应文本详情请求
@app.route('/detail',methods=['GET','POST'])
def author_detail():
    author_name = dict(request.form)["author"][0]
    f_s = open("./create/song/authors.json",'r',encoding='utf-8')
    temp = json.load(f_s)
    for k in range(len(temp)):
        if temp[k]["name"] == author_name:
            return temp[k]["desc"]
    f_t = open("./create/tang/authors.json",'r',encoding='utf-8')
    temp1 = json.load(f_t)
    for k in range(len(temp1)):
        if temp1[k]["name"] == author_name:
            return temp1[k]["desc"]
    return "没有找到相关信息！"

@app.route('/',methods=['GET','POST'])
def query_poets():
    request_items  = dict(request.form)
    print(request_items)
    print(request_items["sentence"][0],request_items["type_s"][0])
    result = query(request_items["sentence"][0],request_items["type_s"][0])
    number = len(result)
    if(number>1000):
        result = result[0:1000]
    print(result)
    return jsonify({"number":number,"result":convert_result_for_html(result,request_items["sentence"][0],request_items["type_s"][0])})

if __name__ == '__main__':
    app.run(debug=True,use_reloader=False)
