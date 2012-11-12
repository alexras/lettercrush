class WordTrie(object):
    def __init__(self):
        self.values = []
        self.children = {}

    def __init__(self, dictionary):
        with open(dictionary, 'r') as fp:
            for word in fp:
                word = word.strip().lower()

                if len(word) > 1:
                    self.add(word)

    def add(self, word):
        self._add(word, 0)

    def _add(self, word, index):
        if index == len(word):
            self.values.append(word)
        else:
            letter = word[index]

            if letter not in self.children:
                self.children[letter] = WordTrie()

            self.children[letter]._add(word, index + 1)

    def get(self, letters):
