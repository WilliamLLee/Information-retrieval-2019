##############################
# support query serve for front web system
# filename:query.py
# author:  liwei
# StuID:   1711350
# date:    2019.12.1
##############################

#查询构建
from whoosh import highlight
from whoosh import qparser
from whoosh import index
from flask import Flask
from flask import request
from flask import jsonify,render_template,abort, redirect, url_for,session, escape
from flask_cors import  *

app = Flask(__name__)
CORS(app,supports_credentials=True)    # 解决跨域请求无响应问题

ix = index.open_dir("index")            #打开该目录一遍存储索引文件

@app.route('/',methods=["GET"])
def index():
    return render_template("index.html")

@app.route('/display/',methods=["GET","POST"])
@app.route('/display/<count>&<query>')
def display(count=None,query=None):
    return render_template("display.html",count=count,query=query)

# 基本查询函数，实现前缀、通配、正则匹配，短语、关系运算查询功能
# 基于whoosh的highlighter实现返回高亮查询词块
@app.route('/index',methods=['GET','POST'])
def base_query():
    assert request.path == '/index'
    print(dict(request.form)["query"][0])
    print(dict(request.form))
    query_sentence = dict(request.form)["query"][0]
    print(query_sentence)
    res = []
    with ix.searcher() as searcher:
        query = qparser.QueryParser("content", ix.schema)
        # query.remove_plugin_class(qparser.WildcardPlugin)
        query.add_plugin(qparser.PrefixPlugin())
        # query.remove_plugin()
        query.add_plugin(qparser.WildcardPlugin)
        query.add_plugin(qparser.OperatorsPlugin)
        query.add_plugin(qparser.RegexPlugin)
        query.add_plugin(qparser.PhrasePlugin)
        q = query.parse(query_sentence)
        print(q)
        result = searcher.search(q,limit=20)
        hf = highlight.HtmlFormatter(tagname="span", classname="match", termclass="term")
        print(result)
        for hit in result:
            print(hit["title"])
            print(hit.highlights("content"))
            res.append({"title":hit["title"],
                        "content":hit.highlights("content"),
                        "path":hit["path"]})
        print(len(result))
        print(res)
    count = len(res)
    #return  redirect("display/%d"%count)
    return  jsonify({"data":res,"url":"display/%d&%s"%(count,query_sentence)})



if __name__ == '__main__':
    app.run(debug=True,use_reloader=False)
