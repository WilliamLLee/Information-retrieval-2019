# enron 公司电子邮件检索系统

> 2019 年 10 月 5 日 最新更新 @[jack-lio](https://github.com/Jack-Lio)

![作业要求](../../../../../../乱七八糟的文件/Typora临时文件/作业要求.jpg)

- 项目说明
>项目内容：本系统基于向量空间模型实现对enron公司150位用户50万封电子邮件进行检索
>检索模型：向量空间模型
>编程语言：Python     
>工具包：nltk、flask、elementUI ...
>数据来源：[eron 电子邮件数据集](http://www.cs.cmu.edu/~enron/)
>实现功能：基于发件时间、发件人、收件人、主题、正文对邮件进行检索，同时拓展了功能实现语音检索功能，对系统进行整合优化，建立前端UI界面对系统进行友好调用。

> ***=>整体系统实现流程图***
> ![系统结构](../../../../../../乱七八糟的文件/Typora临时文件/邮件检索系统.jpg)
> ***=>系统启动步骤***     
>
>  1. 解压压缩包，将压缩包加压的文件夹，放在和邮件解压文件夹（邮件解压文件不在作业压缩包中,要自己解压添加，文件的目录结构若未改动则应该运行没有问题）根目录同一路径下,文件树如下所示：
> ```Python
> |-|
> |-enron_mail_20150507
> |		|--- maildir
> |			|--- 邮件用户列表分类
> |-homework  //作业提交压缩包解压
> |		|--- （文件夹解压所之后的程序和中间文件）    
> ```
>  2. 在控制台运性命令`python backend.py `启动flask后端，启动完成后，打开index.html页面即进行查询。（**因索引文件较大，所以启动会耗一些时间，同时保证可用运行内存在4G以内**）
>   3. ***提示：index.html中使用的 js、cs文件来自网络请求，所以在打开前端页面之前保证网络连接OK！***   



## 一 准备工作

### 1.1 数据分析 
从文件可以看出，enron电子邮件数据已经经过了一部分的处理，所有的邮件按照150个用户进行了分类保存，在每个用户的类别文件夹中，还按照邮件的不同类型、来源、以及用户自行定义的邮件分类系统进行了归类存放。
![用户列表目录](../../../../../../乱七八糟的文件/Typora临时文件/用户列表目录.JPG)

![用户邮件分类列表](D:\我的文件\乱七八糟的文件\Typora临时文件\用户邮件分类列表.JPG)

从邮件的内容来看，邮件基本个数格式包括邮件的ID编码、收发时间、发件人、收件人、主题、mime-version（多用途互联网邮件拓展 版本）、信息类型与编码（规定信息类型和采用的编码格式）、编码转换方式声明（content-transfer-encoding）、邮件抄送密送信息、邮件体等等。

![邮寄格式](D:\我的文件\乱七八糟的文件\Typora临时文件\邮件格式.JPG)


### 1.2 文档预处理
此阶段主要是对文档中的邮件文件进行统一的处理，提取文件目录下的所有文件，同时对其进行编号，将文件路径和文件的编号存入mail_list_file.txt文件。
```python
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
```


![文件列表](../../../../../../乱七八糟的文件/Typora临时文件/文件列表.JPG)

之后按照对于邮件的编号对邮件内容进行分域、分词处理，对不同的文本域有不同的分词处理，所用的分词器利用NlTK的分词函数和正则表达式进行，分词器实现的功能有：单词小写正规化，分词，词源恢复等，同时基于Python的counter实现对单词的词频统计。再利用Python具有的dict数据结构，将每个文件的词频统计数据记录到词汇字典当中，字典之后跟着一个数据统计字典，内容为所有该词汇出现的文件编号（key）和出现次数（value）。

以下是相关核心代码：

```python
# 分词&词形还原函数
# sentence 为输入的单词串
# 此函数采用yield 实现迭代器，返回一个单词的迭代器
# 返回值为经过词形还原之后的一个一个的单词或符号
def lemmatize_all(sentence):
    wnl = WordNetLemmatizer()     # 声明一个词形还原器
    for word, tag in nltk.pos_tag(re.findall(r'[0-9]+[:][0-9]+[:][0-9]+|[0-9]+[:][0-9]+|[0-9]+[.][0-9]+|[0-9]+|[A-Za-z]+[-\'][A-Za-z]+|[A-Za-z]+|[@$]+',sentence)):  # 先正则分词，再给不同的词贴上标签
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
def split_lemmatize(sentence,type):
    # 全部转换为小写字符
    sentence_proc = sentence.lower()
    # nltk分词以及词形还原
    words = []
    if type == '-C' or type == '-S':
        words =[i for i in lemmatize_all(sentence_proc) ]       # 基于nltk分词，将结果以列表形式存储
    elif type == '-D':
        words = re.findall(r'[0-9]+[:][0-9]+[:][0-9]+|[0-9]+|[A-Za-z]+',sentence_proc)
    elif type == '-F' or type == '-T':
        words = re.findall(r'[0-9]+[.][0-9]+|[0-9]+|[A-Za-z]+|[@]+',sentence_proc)
    # print(sentence)
    # print(words)
    count = Counter(words)       # 使用counter进行计数，counter继承了Python的字典数据结构能够很好的解决索引问题
    return len(words),count      #返回句子分词和词形还原之后统计的词条总数以及词项频数
   
# 对文件中不同的文本域进行划分的主要代码，核心思想是利用标识的词项区分  （来自函数 split_words）
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

```

## 二 文件索引构建

利用文件预处理实现的分词词频字典，通过计算tf-idf的值，构建文件索引表，同时记录所有的文件的向量空间长度，将构建的索引表存入index.txt文件，将记录的文件不同域的词项向量空间长度存入file_info.txt文件中。
- tf-idf构建和输出函数代码：
```python
      indexf = open(index_path, 'w', encoding='utf-8')  # 打开索引输出文件流
    infof = open(file_info_path, 'w', encoding='utf-8')  # 打开文件输出流，输出文件中不同域文本的向量空间长度
    for item in index_dict.keys():
        df = len(index_dict[item])
        indexf.write(item)
        for temp in index_dict[item].keys():
            index_dict[item][temp] = math.log(file_count_num / df) * (1 + math.log(index_dict[item][temp]))
            words_count_of_file[temp][order[item[-1]]] = words_count_of_file[temp][order[item[-1]]] +math.pow(index_dict[item][temp] ,2)
            indexf.write( format('#'+temp+':%.2f'%index_dict[item][temp]))
        indexf.write('\n')
    for item in words_count_of_file:
        infof.write(item)
        for temp in  range(len(words_count_of_file[item])):
            if temp != 0:
                infof.write( format(',%.4f'%math.sqrt(words_count_of_file[item][temp])))
            else :
                infof.write(','+str(words_count_of_file[item][temp]))
        infof.write('\n')
    infof.close()
    indexf.close()

```
- 文件向量空间长度信息：
![文件向量空间长度信息](../../../../../../乱七八糟的文件/Typora临时文件/词汇信息.JPG)

- 文件索引列表信息
![文件索引信息](../../../../../../乱七八糟的文件/Typora临时文件/词汇列表.JPG)
## 三 检索系统构建
从文件中读取索引列表信息，通过对查询内容进行相同的分词和tf-idf计算，实现对邮件文本的查询。同时进行拓展，利用百度语音的API实现对于输入语音的文本化，利用文本化的内容实现对于相关内容的查询。将查询结果按照匹配度从高到低进行返回输出。
- 语音文本化代码
```python
# 获取语音输入
def get_audio(filepath):
    aa = 'yes' #str(input("=>start recording？   （yes/no） :"))
    if aa == str("yes") :
        CHUNK = 256
        FORMAT = pyaudio.paInt16
        CHANNELS = 1                # 声道数
        RATE = 16000                # 采样率
        RECORD_SECONDS = 10         # 采样时间
        WAVE_OUTPUT_FILENAME = filepath   #文件存储路径
        p = pyaudio.PyAudio()

        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        print("*"*10, "recording begins：please input audio in 20 seconds! ")
        frames = []
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)
        print("*"*10, "recording end\n")

        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        return "succeed recording!"
    elif aa == str("no"):
        exit()
    else:
        return ("incorrect input，please choose again!")
# 获取语音文本化信息
def recognize(sig, rate, token):
    url = "http://vop.baidu.com/server_api"
    speech_length = len(sig)
    speech = base64.b64encode(sig).decode("utf-8")
    mac_address = uuid.UUID(int=uuid.getnode()).hex[-12:]
    rate = rate
    data = {
        "format": "wav",
        "lan": "en",
        "token": token,
        "len": speech_length,
        "rate": rate,
        "speech": speech,
        "cuid": mac_address,
        "channel": 1,
    }
    data_length = len(json.dumps(data).encode("utf-8"))
    headers = {"Content-Type": "application/json",
               "Content-Length": str(data_length)}
    r = requests.post(url, data=json.dumps(data), headers=headers)
    # print(r.json()['result'])
    return r.json()
```
- 查询代码
```python
# 获取键盘输入，进行查询匹配

def  query(q_sentence,index_dict,words_count_of_file,type):
    length,count = split_lemmatize(q_sentence,type)
    score = {}
    file_count_num = len(words_count_of_file.keys())  # 文件数

    for file in words_count_of_file.keys():
        score[file] = 0.0
        for item in count.keys():			# 如果没有语音分析结果，说明录取的音频没有有效的信息，提前退出并返回错误提示
            if item+type not in index_dict.keys():
                continue
            if file in index_dict[item+type].keys():
                w = index_dict[item+type][file]
            else :
                w = 0
            temp = (1+math.log(count[item]))*math.log(file_count_num/len(index_dict[item+type].keys()))*w
            score[file] = score[file] +temp
        a_len = words_count_of_file[file][order[type[-1]]]
        if a_len == 0 :
            score[file] = 0.0
            continue
        score[file] = score[file]/a_len
 # 对计算的结果进行排序处理
    rank_list = sorted(score.items(),key=lambda x:x[1],reverse=True)
    return rank_list
```

## 四 GUI交互搭建【拓展内容】

基于elementUI实现前端页面的构建，利用flask构建后端内容，对Python相关函数进行调用，实现数据交互和检索查询功能整合实现。

- 前端界面

![前端界面](../../../../../../乱七八糟的文件/Typora临时文件/检索界面.JPG)

- 查询显示文本

![显示文本](../../../../../../乱七八糟的文件/Typora临时文件/显示文本.JPG)



##  ***参考资料：***
- [MIME笔记.阮一峰的网络日志.](http://www.ruanyifeng.com/blog/2008/06/mime.html)	
- [nltk官方文档](https://www.nltk.org/#natural-language-toolkit)
- [python文档-了解相关python基础](https://docs.python.org/2/library/collections.html#counter-objects)
- [elementUI文档](https://element.eleme.cn/#/zh-CN/component/icon)
- [flask中文文档](https://dormousehole.readthedocs.io/en/latest/)
- [百度智能云语音识别文档](https://cloud.baidu.com/doc/SPEECH/s/rjwvy5jlx/)

