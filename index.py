from flask import Flask,render_template,request,redirect,url_for,abort,jsonify
from pymongo import MongoClient

client=MongoClient('localhost',27017)
app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html',name='chenlin')

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
    return render_template('index.html',name='error')

@app.route('/one',methods=['GET'])
def one():
    return jsonify({"name":"chenlin"})
if __name__ == '__main__':
    app.run()
