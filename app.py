from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
import certifi

ca = certifi.where()

client = MongoClient('mongodb+srv://test:sparta@cluster0.xgxgqng.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend')
def recommend():
    return render_template('recommend.html')

@app.route('/recommend/post')
def reviews():
    return render_template('review.html')

@app.route("/recommend/post/list", methods=["POST"])
def recomment_post():
    name_receive = request.form['name_give']
    choose_receive = request.form['choose_give']
    url_receive = request.form['url_give']
    comment_receive = request.form['comment_give']

    doc = {
        'name':name_receive,
        'choose':choose_receive,
        'url':url_receive,
        'comment':comment_receive
    }

    db.recommend.insert_one(doc)
    return jsonify({'msg': '등록 완료!'})

@app.route("/recommend/post/list", methods=["GET"])
def recommend_list():
    recommend_list = list(db.recommend.find({}, {'_id':False}))
    return jsonify({'recommends':recommend_list})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)