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
def get_ten_authors():
    frame = get_coll()
    authors = frame.author
    author_counter = Counter(authors)
    maxAuthor = author_counter.most_common(10)
def get_color():
    season = ["春", "夏", "秋", "冬"]
    colors = ["红", "黄", "绿", "蓝", "白", "黑", "紫", "赤", "灰"]
    plant = ["梅", "竹", "兰", "菊", "松", "柳", "枫", "桃", "李", "梨"]
    animal = ["龙", "虎", "马", "牛", "鸡", "狗","鼠", "兔", "猪", "猴", "蛇", "羊", "鱼", "猫"]
    feeling = ["喜", "怒", "悲", "乐", "忧", "思", "惧"]
    frame = get_coll():
    works = frame.works
    str = ""
    allWorks = str.join(works)
    colorDate=[[],[]]
    for c in colors:
        colorDate[0].append(s)
        colorDate[1].append(works_counter[s])
def get_thulac:
    works = get_coll().works
    thu1 = thulac.thulac()
    allText = []
    for it in 

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
