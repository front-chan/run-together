from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
import certifi

ca = certifi.where()

client = MongoClient('mongodb+srv://rgngr:rgngr@cluster0.apj6ogn.mongodb.net/cluster0?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.hanghae99_08

@app.route('/course')
def home():
    return render_template('course.html')

@app.route("/course/post", methods=["POST"])
def post_course():
    url_receive = request.form['url_give']
    desc_receive = request.form['desc_give']
    location_receive = request.form['location_give']

    doc = {
        'url':url_receive,
        'desc':desc_receive,
        'location':location_receive
    }
    db.course.insert_one(doc)

    return jsonify({'msg':'저장 완료!'})

@app.route("/course/list", methods=["GET"])
def show_course():
    course_list = list(db.course.find({}, {'_id': False}))
    return jsonify({'courses':course_list})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)