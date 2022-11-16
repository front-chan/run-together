from flask import Flask, render_template, request, jsonify, redirect, url_for
import certifi
import random
from pymongo import MongoClient

# JWT 토큰을 만들 때 필요한 비밀문자열입니다. 아무거나 입력해도 괜찮습니다.
# 이 문자열은 서버만 알고있기 때문에, 내 서버에서만 토큰을 인코딩(=만들기)/디코딩(=풀기) 할 수 있습니다.
SECRET_KEY = 'SPARTA'

# JWT 패키지를 사용합니다. (설치해야할 패키지 이름: PyJWT)
import jwt

# 토큰에 만료시간을 줘야하기 때문에, datetime 모듈도 사용합니다.
import datetime

# 회원가입 시엔, 비밀번호를 암호화하여 DB에 저장해두는 게 좋습니다.
# 그렇지 않으면, 개발자(=나)가 회원들의 비밀번호를 볼 수 있으니까요.^^;
import hashlib

app = Flask(__name__)

ca = certifi.where()
client = MongoClient('mongodb+srv://rgngr:rgngr@cluster0.apj6ogn.mongodb.net/cluster0?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.hanghae99_08

@app.route('/challenge')
def challenge():
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

@app.route('/course')
def course_home():
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

    count = random.randrange(1,100000000)

    doc = {
        'name':name_receive,
        'choose':choose_receive,
        'url':url_receive,
        'comment':comment_receive,
        'num':count
    }

    db.recommend.insert_one(doc)
    return jsonify({'msg': '등록 완료!'})

@app.route("/recommend/delete", methods=["POST"])
def recommend_del():
    num_receive = request.form['num_give']
    db.recommend.delete_one({'num': int(num_receive)})
    return jsonify({'msg': '삭제 완료!'})

@app.route("/recommend/post/list", methods=["GET"])
def recommend_list():
    recommend_list = list(db.recommend.find({}, {'_id':False}))
    return jsonify({'recommends':recommend_list})

@app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.user.find_one({"id": payload['id']})
        return render_template('login.html', user_info=user_info)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("index", msg="메인 페이지 입니다."))


@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/index')
def page():
    token_receive = request.cookies.get('mytoken')

    try:
        # 로그인 정보
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.user.find_one({"userId": payload["id"]})

        return render_template("index.html", user_info=user_info)

    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))


#################################
##  로그인을 위한 API            ##
#################################

# [회원가입 API]
# id, pw, nickname을 받아서, mongoDB에 저장합니다.
# 저장하기 전에, pw를 sha256 방법(=단방향 암호화. 풀어볼 수 없음)으로 암호화해서 저장합니다.
@app.route('/api/register', methods=['POST'])
def api_register():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    nickname = request.form['nickname_give']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    doc = {
        "userId": id_receive,  # 아이디
        "password": pw_hash,  # 비밀번호
        "nickname": nickname  # 닉네임
    }

    db.user.insert_one(doc)

    return jsonify({'result': 'success'})


# [로그인 API]
# id, pw를 받아서 맞춰보고, 토큰을 만들어 발급합니다.
@app.route('/api/login', methods=['POST'])
def api_login():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    # 회원가입 때와 같은 방법으로 pw를 암호화합니다.
    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    # id, 암호화된pw을 가지고 해당 유저를 찾습니다.
    result = db.user.find_one({'userId': id_receive, 'password': pw_hash})

    # 찾으면 JWT 토큰을 만들어 발급합니다.
    if result is not None:
        # JWT 토큰에는, payload와 시크릿키가 필요합니다.
        # 시크릿키가 있어야 토큰을 디코딩(=풀기) 해서 payload 값을 볼 수 있습니다.
        # 아래에선 id와 exp를 담았습니다. 즉, JWT 토큰을 풀면 유저ID 값을 알 수 있습니다.
        # exp에는 만료시간을 넣어줍니다. 만료시간이 지나면, 시크릿키로 토큰을 풀 때 만료되었다고 에러가 납니다.
        payload = {
            'id': id_receive,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=60 * 60 * 1)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        # token을 줍니다.
        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


# [유저 정보 확인 API]
# 로그인된 유저만 call 할 수 있는 API입니다.
# 유효한 토큰을 줘야 올바른 결과를 얻어갈 수 있습니다.
# (그렇지 않으면 남의 장바구니라든가, 정보를 누구나 볼 수 있겠죠?)
@app.route('/api/nick', methods=['GET'])
def api_valid():
    token_receive = request.cookies.get('mytoken')

    # try / catch 문?
    # try 아래를 실행했다가, 에러가 있으면 except 구분으로 가란 얘기입니다.

    try:
        # token을 시크릿키로 디코딩합니다.
        # 보실 수 있도록 payload를 print 해두었습니다. 우리가 로그인 시 넣은 그 payload와 같은 것이 나옵니다.
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        print(payload)

        # payload 안에 id가 들어있습니다. 이 id로 유저정보를 찾습니다.
        # 여기에선 그 예로 닉네임을 보내주겠습니다.
        user_info = db.user.find_one({'userid': payload['id']}, {'_id': 0})
        return jsonify({'result': 'success', 'nickname': user_info['nick']})
    except jwt.ExpiredSignatureError:
        # 위를 실행했는데 만료시간이 지났으면 에러가 납니다.
        return jsonify({'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'})
    except jwt.exceptions.DecodeError:
        return jsonify({'result': 'fail', 'msg': '로그인 정보가 존재하지 않습니다.'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)