#!/usr/bin/env python3

import sys
from positions import Position, SetGrid, FrozenSetGrid, read_set_grid, rotate_set_grid, flip_set_grid, spin_set_grid, corner_set_grid, translate_set_grid, print_set_grid, StrGrid, print_char_grid
from dataclasses import dataclass
from typing import Iterable

filename = sys.argv[1]

@dataclass
class Tree:
    size: tuple[int, int]
    present_list: list[int]

presents: dict[int, SetGrid] = {}

trees: list[Tree] = []

# turn [1 0 1 0 2 2] into [0 2 4 4 5 5]
def translate_present_list(present_count: list[int]) -> list[int]:
    result: list[int] = []
    for p_id, count in enumerate(present_count):
        result += [p_id] * count
    return result

with open(filename, 'r') as f:
    for line in f:
        line = line.rstrip()
        if line.endswith(':'):
            key: int = int(line.split(':')[0])
            _, _, present = read_set_grid(f)
            presents[key] = present
        else:
            size_s, present_s = line.split(':')
            sizes = [int(s) for s in size_s.split('x')]
            size = (sizes[0], sizes[1])
            present_counts = [int(s) for s in present_s.split()]
            present_list = translate_present_list(present_counts)
            trees.append(Tree(size, present_list))

# make alternate presents

present_shapes: dict[int, set[FrozenSetGrid]] = {}

for p_id, grid in presents.items():
    options: set[FrozenSetGrid] = { frozenset(grid) }
    options.add(frozenset(corner_set_grid(flip_set_grid(grid))))
    spun = { frozenset(corner_set_grid(spin_set_grid(g))) for g in options}
    options |= spun
    turned = { frozenset(corner_set_grid(rotate_set_grid(g))) for g in options}
    options |= turned
    present_shapes[p_id] = options

# taking advantage of the knowledge that all presents are 3x3
def positions_in_grid(size: tuple[int, int]) -> Iterable[Position]:
    w, h = size
    for x in range(w - 2):
        for y in range(h - 2):
            yield ( (x, y) )

# try to fit presents recursively
def fit_presents(tree: Tree, grid_so_far: SetGrid, last_offset: Position, debug_grid: StrGrid, debug_count: int = 0) -> bool:
    remainder = list(tree.present_list)
    present = remainder.pop(0)
    # print(present, chr(debug_count + 48), len(grid_so_far), remainder)
    next_tree: Tree = Tree(tree.size, remainder)
    for offset in positions_in_grid(tree.size):
        if offset <= last_offset:
            continue
        for option in present_shapes[present]:
            test = translate_set_grid(option, offset)
            if test & grid_so_far:
                # collision
                continue
            # print(print_set_grid(3, 3, option))
            new_grid = grid_so_far | test
            new_debug = dict(debug_grid)
            for p in test:
                new_debug[p] = chr(48 + debug_count)
            if len(remainder) == 0:
                print(f"success {present=} {offset=}")
                print(print_char_grid( tree.size[0], tree.size[1], new_debug))
                return True
            this_offset: Position = offset
            if remainder[0] != present:
                this_offset = (-1, -1)
            # print(print_set_grid( tree.size[0], tree.size[1], new_grid))
            # print(f"moving on with {offset=}")
            # print(print_char_grid( tree.size[0], tree.size[1], new_debug))
            if fit_presents(next_tree, new_grid, this_offset, new_debug, debug_count + 1):
                return True
    return False

def simple_fit_presents(tree: Tree, grid_so_far: SetGrid, last_offset: Position, debug_grid: StrGrid, debug_count: int = 0) -> bool:
    # how big is the space?
    available = tree.size[0] * tree.size[1]
    # how big are the presents?
    used = 0
    for present in tree.present_list:
        used += len(presents[present])
    return used <= available

successes = 0
for tree in trees:
    h, w = tree.size
    present_list = tree.present_list
    # print(present_list)
    present_grid: SetGrid = set()
    debug_grid: StrGrid = {}
    success = simple_fit_presents(tree, present_grid, (-1, -1), debug_grid)
    if success:
        successes += 1

print(successes)
