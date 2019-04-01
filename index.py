from flask import Flask, render_template, request, redirect, url_for, abort, jsonify
from pymongo import MongoClient
from pandas import Series, DataFrame
import pandas as pd
import numpy as np
from collections import Counter
import thulac
# import jieba
# import jieba.posseg as pseg
# import jieba.analyse

app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client['test']


def get_coll():
    all = db.t.find({}, {"_id": 0})
    return all


def getAllInfo(all):
    frame = pd.DataFrame(all, columns=['title', 'author', 'works'])
    authors = frame.author
    titles = frame.title
    works = frame.works
    str = ""
    allWorks = str.join(works)
    allAuthor = str.join(authors)
    works_counter = Counter(allWorks)
    maxTen = works_counter.most_common(12)
    author_counter = Counter(authors)
    maxAuthor = author_counter.most_common(10)
    season = ["春", "夏", "秋", "冬"]
    colors = ["红", "黄", "绿", "蓝", "白", "黑", "紫", "赤", "灰"]
    plant = ["梅", "竹", "兰", "菊", "松", "柳", "枫", "桃", "李", "梨"]
    animal = ["龙", "虎", "马", "牛", "鸡", "狗",
              "鼠", "兔", "猪", "猴", "蛇", "羊", "鱼", "猫"]
    feeling = ["喜", "怒", "悲", "乐", "忧", "思", "惧"]
    thu1 = thulac.thulac()
    # text="我爱北京,,,天安门"
    # text = thu1.cut(allWorks)
    # scenes = jieba.analyse.extract_tags(allWorks,topK=10,withWeight=True,allowPOS=('t'))
    # print(scenes)
    allAddress = []
    allTime = []
    allScenes = []
    allText = []
    i = 0
    j = 0
    for it in works:
        text = thu1.cut(it)
        for item in text:
            allText.append(item)
        if(i > 100):
            t = dict({"text": allText})
            db.txt.insert(t)
            allText = []
            i = 0
        i = i + 1
        j = j + 1
        print(j)
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
    # seasonData = [[],[]]
    # colorData = [[],[]]
    # plantData = [[],[]]
    # animalData = [[],[]]
    # feelData = [[],[]]
    # for s in season:
    #     seasonData[0].append(s)
    #     seasonData[1].append(works_counter[s])
    # for c in colors:
    #     colorData[0].append(c)
    #     colorData[1].append(works_counter[c])
    # for p in plant:
    #     plantData[0].append(p)
    #     plantData[1].append(works_counter[p])
    # for a in animal:

    #     animalData[0].append(a)
    #     animalData[1].append(works_counter[a])
    # for f in feeling:
    #     feelData[0].append(f)
    #     feelData[1].append(works_counter[f])

    return maxAuthor


@app.route('/')
def hello_world():
    return render_template('index.html', name='chenlin')

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
    max = getAllInfo(get_coll())
    app.run()
