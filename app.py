#! /usr/bin/env python

import itertools
import string
from collections import defaultdict
import random

from flask import Flask, request, jsonify, render_template


app = Flask(__name__)
app.secret_key = '\x9d\xc6i:\x04\x1b\x1d\xa7\x8co\xb2\xd4a\x02\xbfM'


# DEFAULT_POEM = """Ancient attempts to define poetry such as Aristotle's Poetics focused on the uses of speech in rhetoric drama song and comedy Later attempts concentrated on features such as repetition verse form and rhyme and emphasized the aesthetics which distinguish poetry from more objectively informative prosaic forms of writing"""
# DEFAULT_POEM = 'a as b c cs d ds e f fs g gs'

DEFAULT_POEM = 'a photo has no light of its own but it takes light to be seen every time anyone takes a photo there is that much less light in circulation'



def pairwise(iterable):
    """Iterate over an iterable two items at a time"""
    a, b = itertools.tee(iterable)
    next(b, None)
    return itertools.izip(a, b)


def clean_poem(poem):
    poem = poem.lower()
    poem.translate(string.maketrans('', ''), string.punctuation)
    return poem.split(' ')


def make_word_map(poem):
    word_map = defaultdict(list)
    poem = clean_poem(poem)
    for a, b in pairwise(poem):
        if b not in word_map[a]:
            word_map[a].append(b)
    # Make the whole thing circular
    word_map[poem[-1]].append(poem[0])
    return poem, word_map


# from collections import Counter

# def analyse(word_map):
#     counter = Counter()
#     for w in word_map:
#         counter[w] = len(word_map[w])
#     print



app.poem, app.word_map = make_word_map(DEFAULT_POEM)


@app.route('/api/word')
def list_words():
    return jsonify(words=app.poem)


@app.route('/api/word/<previous_word>')
def get_next(previous_word):
    next_word = random.choice(app.word_map[previous_word])
    following_word = random.choice(app.word_map[next_word])
    return jsonify(
        previous_word=previous_word,
        next_word=next_word,
        following_word=following_word
    )


@app.route('/')
def index():
    return render_template(
        'index.html',
        first_word=app.poem[0]
    )


if __name__ == '__main__':
    app.run(debug=True, port=5000)
