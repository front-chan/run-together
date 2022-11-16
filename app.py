from pymongo import MongoClient
import datetime
from flask import Flask, render_template, jsonify, request
from datetime import datetime

app = Flask(__name__)
client = MongoClient('mongodb+srv://rgngr:rgngr@cluster0.apj6ogn.mongodb.net/cluster0?retryWrites=true&w=majority')
db = client.hanghae99_100108

@app.route('/')
def home():
    return render_template('course.html')

@app.route('/course', methods=['GET'])
def show_course():
    courses = list(db.course.find({}, {'_id': False}))
    return jsonify({'all_course': courses})

@app.route('/course/post', methods=['POST'])
def post_course():
    location_receive = request.form['location_give']
    desc_receive = request.form['desc_give']

    file = request.files["file_give"]

    extension = file.filename.split('.')[-1]

    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')

    filename = f'file-{mytime}'

    save_to = f'static/{filename}.{extension}'
    file.save(save_to)

    doc = {
        'location':location_receive,
        'desc':desc_receive,
        'file': f'{filename}.{extension}',
        'time': today.strftime('%Y.%m.%d')
    }

    db.course.insert_one(doc)

    return jsonify({'msg': '저장 완료!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=8888, debug=True)