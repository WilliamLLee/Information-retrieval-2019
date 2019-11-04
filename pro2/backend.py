# date: 2019年11月3日
# author: lw
# e-mail: lio6218@163.com
# description: 实现后端的处理返回函数，基于flask包

# -*- coding: utf-8 -*-
from flask import Flask, jsonify, render_template,request
from flask_cors import  *

app = Flask(__name__)  # 实例化app对象
CORS(app,supports_credentials=True)    # 解决跨域请求无响应问题


@app.route('/text',methods=['GET','POST'])
def readText():
    path = request.form['path']
    f = open(path,'r',encoding='utf-8')
    str = ''
    for line in f :
        str = str+line
    return str


if __name__ == '__main__':

    app.run(debug=True,use_reloader=False)
