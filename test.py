#!/usr/bin/env python

from board import *
from wordtrie import WordTrie
import pprint

# possible_words, prefix_map = board.possible_words("/usr/share/dict/words")

# pprint.pprint(map(lambda x: x.word, possible_words))

# d = {}

# for key, value in prefix_map.items():
#     d[possible_words[key].word] = map(lambda x: possible_words[x].word, value)

# pprint.pprint(d)

board = Board("mpswnrzlpcemyopbzlkrnhemv")

print "Generating possible words"
possible_words, prefix_map = board.possible_words("/usr/share/dict/words")

print "Running search ..."
print search(board, possible_words, prefix_map, 3)
