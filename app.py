from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://HwangSoojeong:sue000871@cluster0.1scxwoi.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/api/challengRecruit", methods=["POST"])
def challeng_recruit_post():
    title_receive = request.form['challeng_title_give']
    deadline_receive = request.form['challeng_deadline_give']
    start_date_receive = request.form['challeng_start_date_give']
    end_date_receive = request.form['challeng_end_date_give']
    contents_receive = request.form['challeng_contents_give']

    challeng_list = list(db.withrun.find({},{'_id':False}))

    challeng_num = len(challeng_list) + 1

    doc = {
        'challeng_num' : challeng_num,
        'challeng_title': title_receive,
        'challeng_deadline': deadline_receive,
        'challeng_start_date': start_date_receive,
        'challeng_end_date': end_date_receive,
        'challeng_contents': contents_receive
    }

    db.withrun.insert_one(doc)

    return jsonify({'msg': '챌린지가 등록 되었습니다kk.'})

@app.route("/api/challengeList", methods=["GET"])
def challeng_list_get():
    challeng_list = list(db.withrun.find({}, {'_id': False}))

    return jsonify({'challeng': challeng_list})

@app.route("/api/challengJoin", methods=["POST"])
def challeng_join_post():
    challengNum_receive = request.form['challengNum_give']

    return jsonify({'msg': '챌린지 신청 완료'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)