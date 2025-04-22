#!/usr/bin/env python3
import sys

recipe_n = int(sys.argv[1])

board: list[int] = [3, 7]
elves: list[int] = [0, 1]

def advance() -> int:
    recipe_sum = board[elves[0]] + board[elves[1]]
    recipe_digits = [int(c) for c in str(recipe_sum)]
    board.extend(recipe_digits)
    size = len(board)
    for i in range(2):
        e = elves[i]
        elves[i] =(e + 1 + board[e]) % size
    return recipe_sum

while len(board) < recipe_n + 10:
    advance()

answer = board[recipe_n:recipe_n + 10]

print(''.join([str(d) for d in answer]))
