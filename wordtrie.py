class WordTrie(object):
    __slots__ = ('values', 'children')

    def __init__(self):
        self.values = []
        self.children = {}

    @classmethod
    def from_file(self, dictionary):
        trie = WordTrie()

        count = 0

        with open(dictionary, 'r') as fp:
            for word in fp:
                word = word.strip().lower()

                if len(word) > 1:
                    if trie.add(word):
                        count += 1

        print count
        return trie

    def add(self, word):
        a_ord = ord('a')
        z_ord = ord('z') - ord('a')

        index = 0

        curr_trie = self

        while index < len(word):
            letter = ord(word[index]) - a_ord

            if letter < 0 or letter > z_ord:
                return False

            if letter not in curr_trie.children:
                curr_trie.children[letter] = WordTrie()

            curr_trie = curr_trie.children[letter]
            index += 1

        curr_trie.values.append(word)
        return True

    def lookup(self, letters):
        curr_trie = self

        a_ord = ord('a')

        for letter in letters:
            letter = ord(letter) - a_ord

            if letter in curr_trie.children:
                curr_trie = curr_trie.children[letter]
            else:
                return None
        return curr_trie.values
