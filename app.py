from flask import Flask, render_template, request, jsonify
import certifi
from pymongo import MongoClient

app = Flask(__name__)

ca = certifi.where()
client = MongoClient('mongodb+srv://rgngr:rgngr@cluster0.apj6ogn.mongodb.net/cluster0?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.hanghae99_08

@app.route('/challenge')
def home():
    return render_template('challenge.html')

@app.route("/api/challengeRecruit", methods=["POST"])
def challenge_recruit_post():
    title_receive = request.form['challenge_title_give']
    deadline_receive = request.form['challenge_deadline_give']
    start_date_receive = request.form['challenge_start_date_give']
    end_date_receive = request.form['challenge_end_date_give']
    contents_receive = request.form['challenge_contents_give']
    img_receive = request.form['challenge_img_give']

    challenge_list = list(db.challenge.find({},{'_id':False}))

    challenge_num = len(challenge_list) + 1

    doc = {
        'challenge_num': challenge_num,
        'challenge_title': title_receive,
        'challenge_deadline': deadline_receive,
        'challenge_start_date': start_date_receive,
        'challenge_end_date': end_date_receive,
        'challenge_contents': contents_receive,
        'challenge_img': img_receive
    }

    db.challenge.insert_one(doc)

    return jsonify({'msg': '챌린지가 등록 되었습니다.'})

@app.route("/api/challengeList", methods=["GET"])
def challenge_list_get():
    challenge_list = list(db.challenge.find({}, {'_id': False}))

    return jsonify({'challenge': challenge_list})

@app.route("/api/challengeJoin", methods=["POST"])
def challenge_join_post():
    challenge_num_receive = request.form['challengeNum_give']

    return jsonify({'msg': '챌린지 신청 완료'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)