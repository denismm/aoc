#!/usr/bin/env python3
import sys

recipe_target = sys.argv[1]

# list(str) = list of characters in str
board: list[str] = list('37')
elves: list[int] = [0, 1]

def advance() -> int:
    recipe_sum = sum([int(board[e]) for e in elves])
    recipe_digits = str(recipe_sum)
    board.extend(list(recipe_digits))
    size = len(board)
    for i in range(2):
        e = elves[i]
        elves[i] = (e + 1 + int(board[e])) % size
    return recipe_sum

scan_size = len(recipe_target) + 2
while recipe_target not in ''.join(board[-scan_size:]):
    advance()

print(''.join(board).find(recipe_target))
