#!/usr/bin/env python3
import sys
from typing import Sequence
import functools

filename = sys.argv[1]
with open(filename, "r") as f:
    forest: list[str] = [line.rstrip() for line in f]

height = len(forest)
width = len(forest[0])

def tree(location:Sequence[int]) -> str:
    return forest[location[0]][location[1]]

global top_tree
top_tree: tuple[int, str, tuple[int, int], list[int]] = (0, '!', (0,0), [])
# value, tree, location, scores

directions: list[tuple[int, int]] = [ (1, 0), (0, 1), (-1, 0), (0, -1) ]
def score_location( location:tuple[int, int] ) -> None:
    global top_tree
    treehouse_elevation = tree(location)
    direction_scores:list[int] = []
    for direction in directions:
        trees_seen:int = 0
        pointer = list(location)
        while True:
            pointer = [ c + d for c,d in zip(pointer, direction)]
            if not (0 <= pointer[0] < height and 0 <= pointer[1] < width):
                break
            trees_seen += 1
            if tree(pointer) >= treehouse_elevation:
                break
        direction_scores.append(trees_seen)
    score = functools.reduce(lambda a, b: a * b, direction_scores)
    if score > top_tree[0]:
        top_tree = (score, treehouse_elevation, location, direction_scores)

for x in range(height):
    for y in range(width):
        score_location((x, y))

print(top_tree)

