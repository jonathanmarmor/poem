import glob
import random
import numpy as np
from andreasmusic import audio

audio_dir = 'static/audio'

words = '''
a photo has no light of its own but it takes light to be seen
every time anyone takes a photo there is that much less light in circulation
'''.split()

notes = {
    'a'           : ['C 3'],
    'photo'       : ['D 3'], # d c
    'has'         : ['E 3'],
    'no'          : ['G 3'],
    'light'       : ['Bb2'],
    'of'          : ['E 3'],
    'its'         : ['D 3'],
    'own'         : ['E 3'],
    'but'         : ['G 3'],
    'it'          : ['A 3'],
    'takes'       : ['C 4'],
    'to'          : ['Eb3'],
    'be'          : ['G 3'],
    'seen'        : ['Bb3'],
    'every'       : ['G 3'], # g a
    'time'        : ['G 3'],
    'anyone'      : ['E 3'], # e f e
    'there'       : ['C 3'],
    'is'          : ['Bb2'],
    'that'        : ['D 3'],
    'much'        : ['E 3'],
    'less'        : ['D 3'],
    'in'          : ['C 3'],
    'circulation' : ['D 3'], # d c bb c
}

nplayers = 60
ngrams = (zip(words[:-1], words[1:]))
ngrams.append((words[-1], words[0]))

SR = 44100
LENGTH = SR * 1.2
TIME = 30

class Player(object):

    def __init__(self):
        self.previous_word = random.choice(words)
        self.word = random.choice([b for a, b in ngrams if a == self.previous_word])
        self.note = random.choice(notes[self.word])
        self.position = random.random()
        self.volume = .3
        self.playing = False
        self.will_play = False

    def play(self):
        self.will_play = True

    def step(self):
        self.playing = self.will_play
        self.will_play = False

    def can_hear(self, other):
        should_hear = self.position - other.position < other.volume
        if np.random.random() < .1:
            should_hear = not should_hear
        return should_hear

def read_sung_words():
    sung_words = {}
    filenames = glob.glob('%s/*.wav' % audio_dir)
    for filename in filenames:
        word = filename.replace('.wav', '').replace(audio_dir, '').replace('reverb-', '')
        sung_words[word] = audio.read(filename)
    return sung_words

def main():
    player0 = Player()
    player0.previous_word = None
    player0.word = words[0]
    player0.note = random.choice(notes[player0.word])
    player0.volume = 1
    player0.position = 0.5
    player0.playing = True

    players = [Player() for _ in range(nplayers)]
    players.append(player0)

    a = audio.Audio(np.zeros(((TIME + 5) * LENGTH, 2)), SR)

    sung_words = read_sung_words()

    for t in range(TIME):

        current_players = []
        for player in players:
            if player.playing:
                amp_left = player.volume * (.5 - np.max((.5 - player.position, 0))) * 2
                amp_right = player.volume * (.5 - np.max((player.position - .5, 0))) * 2
                sung_word = sung_words[player.word].signal[:, 0]
                sung_word = np.vstack((sung_word * amp_left, sung_word * amp_right)).T
                start = t * LENGTH + random.randint(0, LENGTH)
                a.signal[start:min(len(a.signal), start + len(sung_word))] += sung_word

                current_players.append(player)

        print [(p.word, p.note) for p in current_players]

        for player in players:
            for other in players:
                if player == other:
                    continue
                if player.can_hear(other) and other.word == player.previous_word and other.playing:
                    player.play()

        for player in players:
            player.step()

    a.signal = a.signal.astype('float32') / np.max(a.signal)

    return a

if __name__ == '__main__':
    main()
