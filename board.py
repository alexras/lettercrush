from blessings import Terminal
import collections

class Player(object):
    RED = False
    BLUE = True

class Board(object):
    DIMENSION = 5

    def __init__(self, letters):
        assert len(letters) == Board.DIMENSION * Board.DIMENSION

        self.letter = list(letters)
        self.letter_multiset = collections.Counter(self.letter)

class Position(object):
    SQUARE_OWNER = 0
    SQUARE_DEFENDED = 1

    def __init__(self):
        self.owner = [None for i in xrange(Board.DIMENSION * Board.DIMENSION)]
        self.defended = [False for i in xrange(len(self.owner))]
        self.red_score = 0
        self.blue_score = 0

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
