import uuid

from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbrhyme

## HTML
@app.route('/')
def rhyme():
    return render_template('notepad.html')

## HTML 화면 보기
@app.route('/update/<id>')
def homework(id):
    return render_template('update.html', id=id)


## API
@app.route('/lyric', methods=['POST'])
def write_lyric():
    title_receive = request.form['title_give']
    author_receive = request.form['author_give']
    genre_receive = request.form['genre_give']
    text_receive = request.form['text_give']

    id = uuid.uuid4().hex

    doc = {
        'id': id,
        'title': title_receive,
        'author': author_receive,
        'genre': genre_receive,
        'text': text_receive
    }

    db.rhyme.insert_one(doc)

    return jsonify({'result': 'success', 'msg': '가사가 성공적으로 저장되었습니다.'})

## API
@app.route('/lyric/<id>', methods=['PATCH'])
def update_lyric(id):
    title_receive = request.form['title_give']
    author_receive = request.form['author_give']
    genre_receive = request.form['genre_give']
    text_receive = request.form['text_give']

    found_rhyme = db.rhyme.find_one({'id': id})

    if found_rhyme is not None:
        doc_to_update = {
            'title': title_receive,
            'author': author_receive,
            'genre': genre_receive,
            'text': text_receive
        }

        db.rhyme.update_one({'id': id}, {'$set': doc_to_update})

        return jsonify({'result': 'success', 'msg': '가사가 성공적으로 저장되었습니다.'})
    else:
        return jsonify({'result': 'failed', 'msg': 'id' + id + '번에 대해서 값을 찾지 못했습니다.'})

@app.route('/lyric', methods=['GET'])
def read_lyric():
    lyrics = list(db.rhyme.find({}, {'_id': 0}))
    return jsonify({'result': 'success', 'lyrics': lyrics})

@app.route('/lyric/<id>', methods=['DELETE'])
def delete_lyric(id):
    print(id)
    db.rhyme.delete_one({'id': id})
    return jsonify({'result': 'success'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)