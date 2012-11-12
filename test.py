#!/usr/bin/env python

from board import *
from wordtrie import WordTrie
import pprint

board = Board("mpswnrzlpcemyopbzlkrnhemv")

possible_words, prefix_map = board.possible_words("/usr/share/dict/words")

pprint.pprint(map(lambda x: x.word, possible_words))

d = {}

for key, value in prefix_map.items():
    d[possible_words[key].word] = map(lambda x: possible_words[x].word, value)

pprint.pprint(d)
