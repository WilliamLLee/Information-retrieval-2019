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
from flask import jsonify,render_template,abort, redirect, url_for,session, escape,Markup
from flask_cors import  *
import re
import logging
from numpy import std
from data import xy_dict
from data import get_html,get_teacher_info,pagerank

# from audio import *

app = Flask(__name__)
CORS(app,supports_credentials=True)    # 解决跨域请求无响应问题
app.secret_key=b'\xfa\n\x08\xb9\x84I\xe5xRdE\xea\x9f\xba\xce\x81'
mysession =dict()                      # 自定义的session用来传输数据
url_dict,scores = pagerank(get_teacher_info())      # 获取pageranke计算结果，返回链接映射和排名得分

# 定义日志记录文件的配置
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"

logging.basicConfig(filename='my.log', level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT)



ix = index.open_dir("index")            #打开该目录一遍存储索引文件

# 网页快照路由
@app.route('/snapshots/<xueyuan>/<filename>',methods=["GET"])
def snapshots(xueyuan = None ,filename=None):
    if filename!=None and xueyuan !=None:
        return render_template('snapshots/'+xueyuan+'/'+filename)
# 主页路由
@app.route('/',methods=["GET"])
def index():
    return render_template("index.html",query="")
# 结果展示页面路由
@app.route('/display/',methods=["GET","POST"])
def display_index():
    return render_template("display.html",count="#",query="输入查询词")

# 结果展示get请求页面响应
@app.route('/display/<count>&<query>')
def display(count=None,query=None):
    #print(query)
    if 'data' in mysession.keys():
        #print(mysession["data"])
        return render_template("display.html",count=count,query=query,res=mysession['data'])
    else:
        return redirect('/display/')


# # 实现语音输入查询
# @app.route('/audio',methods=['GET','POST'])
# def audio_query():
#     assert request.path == '/audio'
#     # 通过语音识别API获取查询输入
#     get_audio(in_path)
#     # 测试代码
#     filename = "./speechs/input.wav"
#     signal = open(filename, "rb").read()
#     rate = 16000
#     token = get_token()
#     msg = recognize(signal, rate, token)
#     query_sentence = " "
#     if "err_no" in dict(msg).keys():
#         logging.warning("%d,没有获取有效语音输入！错误消息%s 错误代码%d" %( 404,msg["err_msg"],msg["err_no"]))
#         return "%d,没有获取有效语音输入！错误消息%s 错误代码%d" %( 404,msg["err_msg"],msg["err_no"]), 404
#     else:
#         query_sentence = msg['result']
#     # 记录日志
#     logging.info("Audio Query sentence: %s" % query_sentence)
#     res = []
#     with ix.searcher() as searcher:
#         # 对输入的查询文本进行解析，如果存在按域查询的需求则区分按域查询，默认采用多属性查询模式
#         # mark 表示是否需要高亮学院查询区域，默认情况下需要
#         highlight_xy = True
#         # 默认的多域查询
#         query = qparser.MultifieldParser(["content", "title", "mtext", "xueyuan"], ix.schema)
#         if query_sentence.endswith("$姓名$"):
#             # 按名字查询
#             query = qparser.SimpleParser("title", ix.schema)
#             query_sentence = query_sentence.strip('$姓名$')
#         elif query_sentence.endswith("$学院$"):
#             # 按学院查询
#             query = qparser.SimpleParser("xueyuan", ix.schema)
#             query_sentence = query_sentence.strip('$学院$')
#
#         elif query_sentence.endswith("$网页$"):
#             # 按网页内容查询
#             query = qparser.SimpleParser("content", ix.schema)
#             query_sentence = query_sentence.strip('$网页$')
#
#         # print(query_sentence)
#         # 引入查询解析器插件
#         query.add_plugin(qparser.WildcardPlugin)
#
#         # query.remove_plugin_class(qparser.WildcardPlugin)
#         query.add_plugin(qparser.PrefixPlugin())
#         query.add_plugin(qparser.OperatorsPlugin)
#         query.add_plugin(qparser.RegexPlugin)
#         query.add_plugin(qparser.PhrasePlugin)
#
#         # 解析得到查询器
#         q = query.parse(query_sentence)
#         logging.info("Query parse result: %s" % str(q))
#         print(q)
#         # 获取查询结果
#         result = searcher.search(q, limit=20)
#         # print(result)
#         # 设置碎片的属性
#         # Allow larger fragments
#         my_cf = highlight.ContextFragmenter(maxchars=200, surround=30)
#         hf = highlight.HtmlFormatter(tagname='em', classname='match', termclass='term')
#
#         hi = highlight.Highlighter(fragmenter=my_cf, formatter=hf)
#         for hit in result:
#             print(hit["picpath"])
#             print(hit["title"])
#             print(escape(hi.highlight_hit(hit, "content")))
#             if hit['picpath'] == '#':
#                 if highlight_xy:
#                     res.append({"title": hit['title'],
#                                 "xueyuan": Markup(hi.highlight_hit(hit, "xueyuan")),
#                                 "url": hit["url"],
#                                 'shotpath': hit['shotpath'],
#                                 "content": Markup(hi.highlight_hit(hit, "content")),
#                                 "parenturl": hit["parenturl"],
#                                 "picpath": '#',
#                                 "pagerank": scores[url_dict[hit["url"]]]
#                                 })
#                 else:
#                     res.append({"title": hit['title'],
#                                 "xueyuan": hit["xueyuan"],
#                                 "url": hit["url"],
#                                 'shotpath': hit['shotpath'],
#                                 "content": Markup(hi.highlight_hit(hit, "content")),
#                                 "parenturl": hit["parenturl"],
#                                 "picpath": '#',
#                                 "pagerank": scores[url_dict[hit["url"]]]
#                                 })
#             else:
#                 if highlight_xy:
#                     res.append({"title": hit['title'],
#                                 "xueyuan": Markup(hi.highlight_hit(hit, "xueyuan")),
#                                 "url": hit["url"],
#                                 'shotpath': hit['shotpath'],
#                                 "content": Markup(hi.highlight_hit(hit, "content")),
#                                 "parenturl": hit["parenturl"],
#                                 "picpath": "images/%s/%s" % (
#                                     hit['picpath'].split('/')[-3], hit['picpath'].split('/')[-1]),
#                                 "pagerank": scores[url_dict[hit["url"]]]
#                                 })
#                 else:
#                     res.append({"title": hit['title'],
#                                 "xueyuan": hit["xueyuan"],
#                                 "url": hit["url"],
#                                 'shotpath': hit['shotpath'],
#                                 "content": Markup(hi.highlight_hit(hit, "content")),
#                                 "parenturl": hit["parenturl"],
#                                 "picpath": "images/%s/%s" % (
#                                     hit['picpath'].split('/')[-3], hit['picpath'].split('/')[-1]),
#                                 "pagerank": scores[url_dict[hit["url"]]]
#                                 })
#         print(len(result))
#         print(res)
#     count = len(result)
#
#     if count == 0:
#         logging.warning("%d,没有查询到相关内容！" % 404)
#         return "没有查询到相关内容！", 404
#     else:
#         # 记录查询日志
#         log = "Response: "
#         for item in res:
#             log = log + " (name:%s,url:%s) " % (item["title"], item["url"])
#         logging.info(log)
#
#         # # 基于page rank 对链接进行排序
#         # res.sort(key=lambda k:(k.get("pagerank",0)),reverse = True)
#         # print(res)
#
#         mysession["data"] = res  # 使用会话session传递参数
#         return jsonify({"url": "/display/%d&%s" % (count, query_sentence)})



# 基本查询函数，实现前缀、通配、正则匹配，短语、关系运算查询功能
# 基于whoosh的highlighter实现返回高亮查询词块
@app.route('/index',methods=['GET','POST'])
def base_query():
    assert request.path == '/index'
    #print(dict(request.form)["query"][0])
    #print(dict(request.form))
    query_sentence = str(dict(request.form)["query"][0])
    logging.info("Query sentence: %s"%query_sentence)
    res = []
    with ix.searcher() as searcher:
        # 对输入的查询文本进行解析，如果存在按域查询的需求则区分按域查询，默认采用多属性查询模式
        # mark 表示是否需要高亮学院查询区域，默认情况下需要
        highlight_xy = True
        # 默认的多域查询
        query = qparser.MultifieldParser(["content","title","mtext","xueyuan"], ix.schema)
        if query_sentence.endswith("$姓名$"):
            # 按名字查询
            query =qparser.SimpleParser("title",ix.schema)
            query_sentence=query_sentence.strip('$姓名$')
        elif query_sentence.endswith("$学院$"):
            # 按学院查询
            query = qparser.SimpleParser("xueyuan", ix.schema)
            query_sentence=query_sentence.strip('$学院$')

        elif query_sentence.endswith("$网页$"):
            # 按网页内容查询
            query = qparser.SimpleParser("content", ix.schema)
            query_sentence=query_sentence.strip('$网页$')

        #print(query_sentence)
        # 引入查询解析器插件
        query.add_plugin(qparser.WildcardPlugin)

        # query.remove_plugin_class(qparser.WildcardPlugin)
        query.add_plugin(qparser.PrefixPlugin())
        query.add_plugin(qparser.OperatorsPlugin)
        query.add_plugin(qparser.RegexPlugin)
        query.add_plugin(qparser.PhrasePlugin)

        # 解析得到查询器
        q = query.parse(query_sentence)
        logging.info("Query parse result: %s"%str(q))
        print(q)
        # 获取查询结果
        result = searcher.search(q,limit=20)
        # print(result)
        # 设置碎片的属性
        # Allow larger fragments
        my_cf = highlight.ContextFragmenter(maxchars=200, surround=30)
        hf = highlight.HtmlFormatter( tagname='em', classname='match', termclass='term')

        hi = highlight.Highlighter(fragmenter=my_cf,formatter=hf)
        for hit in result:
            print(hit["picpath"])
            print(hit["title"])
            print(escape(hi.highlight_hit(hit,"content")))
            if hit['picpath'] =='#':
                if highlight_xy:
                    res.append({"title": hit['title'],
                            "xueyuan": Markup(hi.highlight_hit(hit, "xueyuan")),
                            "url": hit["url"],
                            'shotpath': hit['shotpath'],
                            "content": Markup(hi.highlight_hit(hit, "content")),
                            "parenturl": hit["parenturl"],
                            "picpath": '#',
                            "pagerank":scores[url_dict[hit["url"]]]
                            })
                else:
                    res.append({"title": hit['title'],
                                "xueyuan": hit["xueyuan"],
                                "url": hit["url"],
                                'shotpath': hit['shotpath'],
                                "content": Markup(hi.highlight_hit(hit, "content")),
                                "parenturl": hit["parenturl"],
                                "picpath": '#',
                                "pagerank":scores[url_dict[hit["url"]]]
                                })
            else:
                if highlight_xy:
                     res.append({"title":hit['title'],
                        "xueyuan":Markup(hi.highlight_hit(hit, "xueyuan")),
                        "url":hit["url"],
                        'shotpath':hit['shotpath'],
                        "content":Markup(hi.highlight_hit(hit,"content")),
                        "parenturl": hit["parenturl"],
                        "picpath":"images/%s/%s"%(hit['picpath'].split('/')[-3],hit['picpath'].split('/')[-1]),
                        "pagerank": scores[url_dict[hit["url"]]]
                        })
                else:
                    res.append({"title": hit['title'],
                                "xueyuan": hit["xueyuan"],
                                "url": hit["url"],
                                'shotpath': hit['shotpath'],
                                "content": Markup(hi.highlight_hit(hit, "content")),
                                "parenturl": hit["parenturl"],
                                "picpath": "images/%s/%s" % (
                                hit['picpath'].split('/')[-3], hit['picpath'].split('/')[-1]),
                                "pagerank": scores[url_dict[hit["url"]]]
                                })
        print(len(result))
        print(res)
    count = len(result)

    if count ==0:
        logging.warning("%d,没有查询到相关内容！"%404)
        return "没有查询到相关内容！",404
    else:
        # 记录查询日志
        log = "Response: "
        for item in res:
            log = log + " (name:%s,url:%s) " % (item["title"], item["url"])
        logging.info(log)

        # # 基于page rank 对链接进行排序
        # res.sort(key=lambda k:(k.get("pagerank",0)),reverse = True)
        # print(res)

        mysession["data"] = res                       # 使用会话session传递参数
        return  jsonify({"url":"/display/%d&%s"%(count,query_sentence)})


if __name__ == '__main__':
    app.run(debug=False,use_reloader=False)

