from blessings import Terminal
import collections, itertools

class Player(object):
    RED = False
    BLUE = True

    @classmethod
    def opponent(self, player):
        return not player

    @classmethod
    def negamax_color(self, player):
        if player == Player.RED:
            return -1
        else:
            return 1

class WordInfo(object):
    __slots__ = ('letters', 'word')

    def __init__(self, letters, word):
        self.letters = letters
        self.word = word

class Board(object):
    DIMENSION = 5

    def __init__(self, letters):
        assert len(letters) == Board.DIMENSION * Board.DIMENSION

        self.letter = list(letters)

    def possible_words(self, dictionary_file):
        sorted_letters = sorted(self.letter)

        words = []

        with open(dictionary_file, 'r') as fp:
            for word in fp:
                word = word.strip().lower()

                if len(word) < 2:
                    continue

                # Assumes words are sorted in lexicographical order; doesn't
                # capture all ways of spelling the same word

                sorted_word = sorted(word)

                word_index = 0
                letter_index = 0

                letters = []

                while (word_index < len(sorted_word) and
                       letter_index < len(sorted_letters)):
                    if sorted_word[word_index] == sorted_letters[letter_index]:
                        word_index += 1
                        letters.append(letter_index)

                    letter_index += 1

                if word_index == len(word):
                    if len(words) == 0 or words[-1].word != word:
                        words.append(WordInfo(letters, word))

        # Construct a map of which words are prefixes of other words
        prefix_map = {}

        for i, word_info in enumerate(words):
            for j in xrange(i + 1, len(words)):
                if words[j].word[:len(word_info.word)] == word_info.word:
                    if j not in prefix_map:
                        prefix_map[j] = []
                    prefix_map[j].append(i)

        return (words, prefix_map)

class Position(object):
    SQUARE_OWNER = 0
    SQUARE_DEFENDED = 1

    def __init__(self):
        self.owner = [None for i in xrange(Board.DIMENSION * Board.DIMENSION)]
        self.defended = [False for i in xrange(len(self.owner))]
        self.red_score = 0
        self.blue_score = 0

    def __hash__(self):
        # Hash is a base-3 number representing the state of the board
        my_hash = 0

        for owner in self.owner:
            if owner == RED:
                my_hash += 1
            elif owner == BLUE:
                my_hash += 2
            my_hash *= 3

    def copy(self):
        other = Position()

        other.owner = list(self.owner)
        other.defended = list(self.defended)
        other.red_score = self.red_score
        other.blue_score = self.blue_score

        return other

    def update(self, player, letter_indices):
        for index in letter_indices:
            self.owner[index] = player

        self.red_score = 0
        self.blue_score = 0

        for cell in xrange(len(self.owner)):
            cell_owner = self.owner[cell]

            defended = True

            if cell_owner is None:
                defended = False
            else:
                if cell_owner == Player.RED:
                    self.red_score += 1
                else:
                    self.blue_score += 1

                for neighbor in self.neighbors(cell):
                    if self.owner[neighbor] != cell_owner:
                        defended = False

            self.defended[cell] = defended

    def score(self):
        return (self.blue_score, self.red_score)

    def endgame(self):
        for cell_owner in self.owner:
            if cell_owner is None:
                return False
        return True

    def neighbors(self, x):
        if x > 0:
            yield x - 1

        if x + 1 < Board.DIMENSION * Board.DIMENSION:
            yield x + 1

        if x  >= Board.DIMENSION:
            yield x - Board.DIMENSION

        if (x + Board.DIMENSION < Board.DIMENSION * Board.DIMENSION):
            yield x + Board.DIMENSION

def print_board(board, position):
    board_str = ""

    term = Terminal()

    for x in xrange(Board.DIMENSION):
        for y in xrange(Board.DIMENSION):
            index = x * Board.DIMENSION + y

            square_owner = position.owner[index]
            square_letter = board.letter[index]
            square_defended = position.defended[index]

            if square_owner is None:
                board_str += term.white
            elif square_owner == Player.RED:
                if square_defended:
                    board_str += term.bold_white_on_bright_red
                else:
                    board_str += term.white_on_red
            else:
                if square_defended:
                    board_str += term.bold_white_on_bright_blue
                else:
                    board_str += term.white_on_blue

            board_str += square_letter.upper() + term.normal
        board_str += "\n"

    blue_score, red_score = position.score()

    board_str += term.white_on_bright_blue(str(blue_score))
    board_str += " / "
    board_str += term.white_on_bright_red(str(red_score))
    board_str += '\n'

    print board_str

# Depth-limited negamax pruning
def search_sub(possible_words, available_words, prefix_map, player, position,
               alpha, beta, depth, known_scores):

    if depth == 0 or position.endgame() or len(available_words) == 0:
        if player == Player.BLUE:
            return (Player.negamax_color(player) * position.blue_score, [])
        else:
            return (Player.negamax_color(player) * position.red_score, [])

    best_word_list = None

    for word_index in available_words:
        # Calculate the next position given the word, and the remaining set of
        # words available subject to the rules

        next_position = position.copy()
        next_position.update(player, possible_words[word_index].letters)

        remaining_words = set(available_words)

        word_stack = [word_index]

        while len(word_stack) > 0:
            next_word = word_stack.pop()

            remaining_words.discard(next_word)

            if next_word in prefix_map:
                for prefix in prefix_map[next_word]:
                    word_stack.append(prefix)


        (score, word_list) = search_sub(
            possible_words, remaining_words, prefix_map,
            Player.opponent(player), next_position, -1 * beta, -1 * alpha,
            depth - 1)

        score = -1 * score

        word_list.append(word_index)

        if score >= beta:
            return (score, word_list)

        if score >= alpha:
            alpha = score
            best_word_list = word_list

    return (alpha, best_word_list)


def search(board, possible_words, prefix_map, depth):
    position = Position()

    available_words = set(range(len(possible_words)))

    player = Player.BLUE
    initial_position = Position()

    known_scores = {
        Player.RED : {},
        Player.BLUE : {}
        }

    # Board.DIMENSION ^2 + 1 is effectively infinity, since it's larger than
    # any possible score
    infinity = (Board.DIMENSION * Board.DIMENSION) + 1

    score, word_list = search_sub(
        possible_words, available_words, prefix_map, player, initial_position,
        -1 * infinity, infinity, depth, known_scores)

    word_list.reverse()

    return (possible_words[word_list[0]].word,
            map(lambda x: possible_words[x].word, word_list))
