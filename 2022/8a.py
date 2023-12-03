#!/usr/bin/env python3
import sys
from typing import Sequence, Iterable

filename = sys.argv[1]
with open(filename, "r") as f:
    forest: list[str] = [line.rstrip() for line in f]

visible: set[tuple[int, int]] = set()


def find_trees(  # type: ignore[no-untyped-def]
    row_function=enumerate,
    tree_function=enumerate,
    sideways=False,
) -> None:
    for y, row in row_function(forest):
        current_max = "!"  # less than number characters
        for x, tree in tree_function(row):
            if current_max < tree:
                if sideways:
                    visible.add((y, x))
                else:
                    visible.add((x, y))
                current_max = tree


def backwards(row: Sequence[str]) -> Iterable[tuple[int, str]]:
    for i in reversed(range(len(row))):
        yield (i, row[i])


def sideways(forest: Sequence[str]) -> Iterable[tuple[int, list[str]]]:
    for x in range(len(forest[0])):
        yield x, [forest[y][x] for y in range(len(forest))]


# from west
find_trees()
# from east
find_trees(tree_function=backwards)
# from north
find_trees(row_function=sideways, sideways=True)
# from south
find_trees(row_function=sideways, tree_function=backwards, sideways=True)
print(len(visible))
