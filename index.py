from flask import Flask, render_template, request, redirect, url_for, abort, jsonify
from pymongo import MongoClient
from pandas import Series, DataFrame
import pandas as pd
import numpy as np
from collections import Counter
import thulac
from gensim.models import word2vec
import re
import json
# import jieba
# import jieba.posseg as pseg
# import jieba.analyse

app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client['test2']


# 获取全唐诗内容
def get_coll():
    all = db.t.find({}, {"_id": 0})
    frame = pd.DataFrame(all, columns=['title', 'author', 'works'])
    return frame
# 获取字的排行存入数据库中


def get_word():
    frame = get_coll()
    works = frame.works
    str = ""
    allWorks = str.join(works)
    works_counter = Counter(allWorks)
    maxTen = works_counter.most_common(12)
    db.show.insert_one({"word": maxTen})
# 获取作者的排行存入数据库中


def get_ten_authors():
    frame = get_coll()
    authors = frame.author
    author_counter = Counter(authors)
    maxAuthor = author_counter.most_common(10)
    db.show.insert_one({"author": maxAuthor})
# 获取季节，植物，动物的排行存入数据中


def get_season():
    season = ["春", "夏", "秋", "冬"]
    plant = ["梅", "竹", "兰", "菊", "松", "柳", "枫", "桃", "李", "梨"]
    animal = ["龙", "虎", "马", "牛", "鸡", "狗",
              "鼠", "兔", "猪", "猴", "蛇", "羊", "鱼", "猫"]
    frame = get_coll()
    works = frame.works
    str = ""
    allWorks = str.join(works)
    works_counter = Counter(allWorks)
    seasonDate = {}
    for s in season:
        seasonDate[s] = works_counter[s]
    plantDate = {}
    for p in plant:
        plantDate[p] = works_counter[p]
    animalDate = {}
    for a in animal:
        animalDate[a] = works_counter[a]
    s = dict({"season": seasonDate})
    p = dict({"plant": plantDate})
    a = dict({"animal": animalDate})
    all = [a, p, s]
    db.show.insert_many(all)
# 获取唐诗情感排行


def get_feelings():
    # like喜,fun乐,fear惧,angry怒,think思,sad悲,worry,忧
    like = ["喜", "健", "倩", "贺", "好", "良", "善"]
    fun = ["悦", "欣", "乐", "怡", "洽", "畅", "愉"]
    fear = ["谗", "谤", "患", "罪", "诈", "惧", "诬"]
    angry = ["怒", "雷", "吼", "霆", "霹", "猛", "轰"]
    think = ["思", "忆", "怀", "恨", "吟", "逢", "期"]
    sad = ["愁", "恸", "痛", "寡", "哀", "伤", "嗟"]
    worry = ["恤", "忧", "痾", "虑", "艰", "遑", "厄"]
    feels = {}
    feels["喜"] = get_single_color(like)
    feels["乐"] = get_single_color(fun)
    feels["惧"] = get_single_color(fear)
    feels["怒"] = get_single_color(angry)
    feels["思"] = get_single_color(think)
    feels["悲"] = get_single_color(sad)
    feels["忧"] = get_single_color(worry)
    f = dict({"feels": feels})
    db.show.insert(f)

    # 获取唐诗颜色的排行


def get_colors():
    red = ["红", "赤", "丹", "朱", "殷", "绛", "檀", "翡", "彤",
           "绯", "缇", "茜", "赪", "赭", "赩", "赮", "骍", "纁"]
    white = ["白", "素", "皎", "皓", "皙"]
    yellow = ["黄", "黈", "缃"]
    green = ["绿", "青", "碧", "翠", "苍", "綦", ]
    black = ["黑", "暗", "玄", "乌", "冥", "墨", "褐", "黛", "黎", "黯", "皂", "淄", "黝"]
    blue = ["蓝", "靛", "雘"]
    other = ["紫", "灰"]
    colors = {}
    colors["red"] = get_single_color(red)
    colors["white"] = get_single_color(white)
    colors["yellow"] = get_single_color(yellow)
    colors["green"] = get_single_color(green)
    colors["black"] = get_single_color(black)
    colors["blue"] = get_single_color(blue)
    colors["other"] = get_single_color(other)
    c = dict({"colors": colors})
    db.show.insert(c)
# 获取单独一个系列的排行


def get_single_color(colors):
    frame = get_coll()
    works = frame.works
    works_counter = Counter("".join(works))
    colorDate = [[], []]
    sum = 0
    for s in colors:
        colorDate[0].append(s)
        number = works_counter[s]
        colorDate[1].append(number)
        sum = sum + number
    return sum


# thulac通用标记集
'''
    n/名词 np/人名 ns/地名 ni/机构名 nz/其它专名
    m/数词 q/量词 mq/数量词 t/时间词 f/方位词 s/处所词
    v/动词 a/形容词 d/副词 h/前接成分 k/后接成分 i/习语
    j/简称 r/代词 c/连词 p/介词 u/助词 y/语气助词
    e/叹词 o/拟声词 g/语素 w/标点 x/其它
'''
# 按类别获取分词结果分类


def get_thulac_par():
    works = get_coll().works
    thu1 = thulac.thulac()
    speech = {}
    i = 0
    names = ["n", "np", "ns", "ni", "nz", "m", "q", "mq", "t", "f", "s", "v", "a",
             "d", "h", "k", "i", "j", "r", "c", "p", "u", "y", "e", "o", "g", "w", "x"]
    for it in works:
        text = thu1.cut(it)
        for item in text:
            for name in names:
                if name == item[1]:
                    if name in speech:
                        speech[name].append(item[0])
                    else:
                        speech[name] = []
        i = i+1
    for s in speech:
        t = dict({s: speech[s]})
        db.speech.insert_one(t)


def get_word_class():
    words = db.speech.find({}, {"_id": 0})


'''
    # 获取唐诗分词结果，一部分存入数据库，一部分写入peo.txt文本.
'''


def get_thulac():
    works = get_coll().works
    thu1 = thulac.thulac()
    allText = []
    i = 0
    j = 0
    file_open = open("peo1.txt", 'a+', encoding='utf-8')
    for it in works:
        text = thu1.cut(it)
        for item in text:
            if item[0] != "，" and item[0] != "。":
                file_open.write(item[0]+" ")
                allText.append(item[0])
        if(i > 100):
            t = dict({"text": allText})
            db.txxt.insert(t)
            allText = []
            i = 0
        i = i + 1
        j = j + 1
    file_open.close()
# 词向量分析


def get_word_vector():
    # frame = get_coll()
    # works = frame.works
    # str = ""
    # allWorks = str.join(works)
    sentences = word2vec.Text8Corpus("peo2.txt")
    model = word2vec.Word2Vec(sentences, min_count=3,
    size=100, window=5, workers=4, seed=0)
    model.save('poetry.model')
    sam = model.most_similar('天子', topn=10)
    print("关键词：天子\n")
    for key in sam:
        print(key[0], key[1])
    sam1 = model.most_similar('寂寞', topn=10)
    print("关键词：寂寞\n")
    for key in sam1:
        print(key[0], key[1])
    sam2 = model.most_similar('李白', topn=10)
    print("关键字：李白\n")
    for key in sam2:
        print(key[0], key[1])
    sam3 = model.most_similar('明月', topn=10)
    print("关键字：明月\n")
    for key in sam3:
        print(key[0], key[1])
    # for i in model.most_similar(u"天子"):
    #     print("0")
    #     print(i[0],i[1])
    # print(allWorks)
    # all = db.thulac.find({},{"_id":0})
    # frame = pd.DataFrame(all,columns=['text'])
    # text = frame.text
    # j = 0
    # vector = []
    # for i in text:
    #     if j !=0:
    #         i = np.array(i)
    #         print(i)
    #     j=j+1
    # print(vector)

# 在线分析词向量


def item_get_similarity(key):
    model = word2vec.Word2Vec.load("poetry.model")
    try:
        sam2 = model.most_similar(key, topn=10)
        return sam2
    except:
        return "该词语没有找到"
    # print("关键字：明月\n")
    # for key in sam2:
    #     print(key[0],key[1])


def getAllInfo(all):
    frame = pd.DataFrame(all, columns=['title', 'author', 'works'])
    authors = frame.author
    titles = frame.title
    works = frame.works
    thu1 = thulac.thulac()
    allAddress = []
    allTime = []
    allScenes = []
    allText = []

    for it, index in works:

        text = thu1.cut(it)
        for item in text:
            allText.append(item)
            # if item[1] == 'ns':
            #     allAddress.append(item[0])
            # if item[1] == 't':
            #     allTime.append(item[0])
            # if item[1] == 's':
            #     allScenes.append(item[0])
    i = 0
    j = 0

    # if item[1] == 'ns':
    #     allText[0].name = item[1]
    #     allText[0].text
    #     allAddress.append(item[0])
    # if item[1] == 't':
    #     allTime.append(item[0])
    # if item[1] == 's':
    #     allScenes.append(item[0])
    #     print(text,allAddress,allTime,allTime)
    # address_counter = Counter(allAddress)
    # time_counter = Counter(allTime)
    # scenes_counter = Counter(allScenes)
    # maxAddress = address_counter.most_common(10)
    # maxTime = time_counter.most_common(10)
    # maxScenes = scenes_counter.most_common(10)
    # for add in maxAddress:
    #     print(add)
    # print('\n')
    # for time in maxTime:
    #     print(time)
    # print('\n')
    # for sce in maxScenes:
    #     print(sce)


@app.route('/')
def hello_world():
    return render_template('index.html')

def get_json(arr):
    return json.loads((arr.decode("utf-8")))

def get_sort_rank(sort):
    # sort = "ns"
    sortAll = db.speech.find({},{"_id":0})
    frame = pd.DataFrame(sortAll)
    #     authors = frame.author
    # author_counter = Counter(authors)
    # maxAuthor = author_counter.most_common(10)
    areas = frame[sort].tolist()
    result = []
    for a in areas:
        if type(a).__name__!='float':
            result.append(a)

    address_counter = Counter(result[0])
    mxaAddress = address_counter.most_common(10)
    # db.show.insert_one({sort: mxaAddress})
    return mxaAddress

#获取分类词向量的排行
@app.route("/sort",methods=['POST'])
def get_sort_word():
    try:
        result = get_sort_rank(get_json(request.get_data('sort'))['sort'])
        data = dict({"data":result})
    except:
        data = dict({"data":"error"})
    return jsonify(data)

# 获取字或词的数量信息。
@app.route("/word", methods=['POST'])
def get_word_online():
    words = get_json(request.get_data('word'))['word']
    print(words)

    frame = get_coll()
    works = frame.works
    str = ""
    allWorks = str.join(works)
    works_counter = Counter(allWorks)
    result = []
    for r in words:
        res = []
        res.append(r)
        res.append(works_counter[r])
        result.append(res)
    data = dict({"data": result})
    return jsonify(data)

#获取词数量接口
@app.route("/trems",methods=['POST'])
def get_trems():
    trems = get_json(request.get_data('trems'))['trems']
    txt = open('peo2.txt',encoding='UTF-8').read()
    new_txt= re.split(" ",txt)
    result = Counter(new_txt)
    data = []
    for t in trems:
        it = []
        it.append(t)
        it.append(result[t])
        data.append(it)
    data = dict({"data":data})
    return jsonify(data)

# 获取词向量相近的前十接口


@app.route("/similarity", methods=['POST'])
def get_similarity():
    k = get_json(request.get_data('key'))
    maxTen = item_get_similarity(k['key'])
    data = dict({"data": maxTen})
    return jsonify(data)

# 获取词向量相近程度接口
@app.route("/degrees", methods=['POST'])
def get_degree():
    degrees = get_json(request.get_data('key'))['key']
    model = word2vec.Word2Vec.load("poetry.model")
    try:
        result = str(model.similarity(degrees[0], degrees[1]))
        data = dict({"data": result})
    except:
        data = dict({"data":"该词语无法找到"})
    return jsonify(data)

# 获取展示数据接口
@app.route('/show')
def get_show():
    show = db.show.find({}, {"_id": 0})
    sum = []
    for i in show:
        sum.append(i)
    data = dict({"data": sum})
    return jsonify(data)
# @app.route('/login',methods=['POST','GET'])
# def login():
#     error = None
#     if request.method=='POST':
#         if valid_login(request.form['username'],request.form['password']):
#             return log_the_user_in(request.form['username'])
#         else:
#             error='Invalid username/password'
#     return render_template('index.html',error=error)


@app.route('/login')
def login():

    return redirect(url_for('error'))


@app.route('/error')
def error():
    abort(401)
    return render_template('index.html', name='error')


@app.route('/one', methods=['GET'])
def one():

    return jsonify({"data": max})

if __name__ == '__main__':
    app.run()
