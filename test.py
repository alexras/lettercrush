#!/usr/bin/env python

from board import *

board = Board("mpswnrzlpcemyopbzlkrnhemv")
position = Position()



position.update(
    Player.RED,
    [0, 1, 2, 7, 11, 15, 17, 19, 22])

position.update(
    Player.BLUE,
    [5, 8, 10, 12, 13, 18])

print_board(board, position)

second_position = Position()

second_position.update(
    Player.RED,
    [10, 11, 12, 6, 16])

print_board(board, second_position)
