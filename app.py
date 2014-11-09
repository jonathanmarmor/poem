#! /usr/bin/env python

import itertools
import string
from collections import defaultdict
import random
import redis

from flask import Flask, request, jsonify, render_template


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

    word_index = app.redis_client.incr(hash) % len(app.words)
    previous_word = app.words[(word_index - 1) % len(app.words)]
    word = app.words[word_index % len(app.words)]

    return render_template(
        'index.html',
        previous_word=previous_word,
        word=word
    )


if __name__ == '__main__':
    app.run(debug=True)
