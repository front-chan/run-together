from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://HwangSoojeong:sue000871@cluster0.1scxwoi.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/api/challengeRecruit", methods=["POST"])
def challenge_recruit_post():
    title_receive = request.form['challenge_title_give']
    deadline_receive = request.form['challenge_deadline_give']
    start_date_receive = request.form['challenge_start_date_give']
    end_date_receive = request.form['challenge_end_date_give']
    contents_receive = request.form['challenge_contents_give']

    challenge_list = list(db.withrun.find({},{'_id':False}))

    challenge_num = len(challenge_list) + 1

    doc = {
        'challenge_num': challenge_num,
        'challenge_title': title_receive,
        'challenge_deadline': deadline_receive,
        'challenge_start_date': start_date_receive,
        'challenge_end_date': end_date_receive,
        'challenge_contents': contents_receive
    }

    db.withrun.insert_one(doc)

    return jsonify({'msg': '챌린지가 등록 되었습니다.'})

@app.route("/api/challengeList", methods=["GET"])
def challenge_list_get():
    challenge_list = list(db.withrun.find({}, {'_id': False}))

    return jsonify({'challenge': challenge_list})

@app.route("/api/challengeJoin", methods=["POST"])
def challenge_join_post():
    challenge_num_receive = request.form['challengeNum_give']

    return jsonify({'msg': '챌린지 신청 완료'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)