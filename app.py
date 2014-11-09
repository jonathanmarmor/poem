#! /usr/bin/env python

import redis
from flask import Flask, render_template

from config import CONF


app = Flask(__name__)
app.secret_key = '\x9d\xc6i:\x04\x1b\x1d\xa7\x8co\xb2\xd4a\x02\xbfM'


app.words = '''
a photo has no light of its own but it takes light to be seen
every time anyone takes a photo there is that much less light in circulation
'''.split()

app.redis_client = redis.Redis()


@app.route('/', defaults={'hash': 'default'})
@app.route('/<hash>')
def index(hash):

    len_words = len(app.words)
    word_index = app.redis_client.incr(hash) % len_words
    previous_word = app.words[(word_index - 1) % len_words]
    word = app.words[word_index]

    return render_template(
        'index.html',
        previous_word=previous_word,
        word=word
    )


if __name__ == '__main__':
    print 'DEBUGGING??????', CONF.DEBUG
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=CONF.DEBUG
    )
