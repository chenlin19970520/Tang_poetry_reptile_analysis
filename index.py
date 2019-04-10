from flask import Flask, render_template, request, redirect, url_for, abort, jsonify
from pymongo import MongoClient
from pandas import Series, DataFrame
import pandas as pd
import numpy as np
from collections import Counter
import thulac
from gensim.models import word2vec
import re
# import jieba
# import jieba.posseg as pseg
# import jieba.analyse

app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client['test']


#获取初级
def get_coll():
    all = db.t.find({}, {"_id": 0})
    frame = pd.DataFrame(all, columns=['title', 'author', 'works'])
    return frame
def get_word():
    frame = get_coll()
    works = frame.works
    str = ""
    allWorks = str.join(works)
    works_counter = Counter(allWorks)
    maxTen = works_counter.most_common(12)
    db.show.insert_one({"word":maxTen})
def get_ten_authors():
    frame = get_coll()
    authors = frame.author
    author_counter = Counter(authors)
    maxAuthor = author_counter.most_common(10)
    db.show.insert_one({"author":maxAuthor})
def get_season():
    season = ["春", "夏", "秋", "冬"]
    plant = ["梅", "竹", "兰", "菊", "松", "柳", "枫", "桃", "李", "梨"]
    animal = ["龙", "虎", "马", "牛", "鸡", "狗","鼠", "兔", "猪", "猴", "蛇", "羊", "鱼", "猫"]
    frame = get_coll()
    works = frame.works
    str = ""
    allWorks = str.join(works)
    works_counter = Counter(allWorks)
    seasonDate= {}
    for s in season:
        seasonDate[s] = works_counter[s]
    plantDate = {}
    for p in plant:
        plantDate[p] = works_counter[p]
    animalDate = {}
    for a in animal:
        animalDate[a] = works_counter[a]
    s = dict({"season":seasonDate})
    p = dict({"plant":plantDate})
    a = dict({"animal":animalDate})
    all = [a,p,s]
    db.show.insert_many(all)

def get_feelings():
    #like喜,fun乐,fear惧,angry怒,think思,sad悲,worry,忧
    like=["喜","健","倩","贺","好","良","善"]
    fun=["悦","欣","乐","怡","洽","畅","愉"]
    fear=["谗","谤","患","罪","诈","惧","诬"]
    angry=["怒","雷","吼","霆","霹","猛","轰"]
    think=["思","忆","怀","恨","吟","逢","期"]
    sad=["愁","恸","痛","寡","哀","伤","嗟"]
    worry=["恤","忧","痾","虑","艰","遑","厄"]
    feels={}
    feels["喜"] = get_single_color(like)
    feels["乐"] = get_single_color(fun)
    feels["惧"] = get_single_color(fear)
    feels["怒"] = get_single_color(angry)
    feels["思"] = get_single_color(think)
    feels["悲"] = get_single_color(sad)
    feels["忧"] = get_single_color(worry)
    f = dict({"feels": feels})
    db.show.insert(f)
def get_colors():
    red = ["红","赤","丹","朱","殷","绛","檀","翡","彤","绯","缇","茜","赪","赭","赩","赮","骍","纁"]
    white=["白","素","皎","皓","皙"]
    yellow=["黄","黈","缃"]
    green=["绿","青","碧","翠","苍","綦",]
    black=["黑","暗","玄","乌","冥","墨","褐","黛","黎","黯","皂","淄","黝"]
    blue=["蓝","靛","雘"]
    other=["紫","灰"]
    colors = {}
    colors["red"] = get_single_color(red)
    colors["white"]  = get_single_color(white)
    colors["yellow"]  = get_single_color(yellow)    
    colors["green"]  = get_single_color(green)
    colors["black"]  = get_single_color(black)
    colors["blue"]  = get_single_color(blue)
    colors["other"]  = get_single_color(other)
    c = dict({"colors": colors})
    db.show.insert(c)

def get_single_color(colors):
    frame = get_coll()
    works = frame.works
    works_counter = Counter("".join(works))
    colorDate = [[],[]]
    sum = 0
    for s in colors:
        colorDate[0].append(s)
        number = works_counter[s]
        colorDate[1].append(number)
        sum = sum + number
    return sum

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

def get_word_vector():
    # frame = get_coll()
    # works = frame.works
    # str = ""
    # allWorks = str.join(works)
    sentences = word2vec.Text8Corpus("peo2.txt")
    model = word2vec.Word2Vec(sentences,min_count=3,size=100,window=5,workers=4,seed=0)
    model.save('poetry.model')
    sam = model.most_similar('天子',topn=10)
    print("关键词：天子\n")
    for key in sam:
        print(key[0],key[1])
    sam1 = model.most_similar('寂寞',topn=10)
    print("关键词：寂寞\n")
    for key in sam1:
        print(key[0],key[1])
    sam2 = model.most_similar('李白',topn=10)
    print("关键字：李白\n")
    for key in sam2:
        print(key[0],key[1])
    sam3 = model.most_similar('明月',topn=10)
    print("关键字：明月\n")
    for key in sam3:
        print(key[0],key[1])
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
def get_similarity():
    model = word2vec.Word2Vec.load("poetry.model")
    sam2 = model.most_similar('明月',topn=10)
    print("关键字：明月\n")
    for key in sam2:
        print(key[0],key[1])

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

    for it,index in works:
        print(index)
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
    return render_template('index.html', name='chenlin')

@app.route('/show')
def get_show():
    word = get_word()
    author = get_ten_authors()
    return jsonify({'word':word,'author':author})
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
    get_ten_authors()
    app.run()
