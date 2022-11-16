import random

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

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)