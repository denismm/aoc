#!/usr/bin/env python3
import sys
from positions import Position, add_direction
from pprint import pprint
from collections import deque

filename = sys.argv[1]

Grid = dict[Position, int]
FlyingBrick = tuple[Position, ...]
Brick = set[Position]

flying_bricks: list[FlyingBrick] = []

down = (0, 0, -1)
up = (0, 0, 1)

with open(filename, "r") as f:
    for line in f:
        line = line.rstrip()
        positions = line.split('~')
        fbrick = tuple(tuple(int(s) for s in p.split(',')) for p in positions)
        # we want lower z first
        flying_bricks.append(tuple(sorted(fbrick, key=lambda pos: pos[2])))
flying_bricks.sort(key=lambda b: b[0][2])

def make_brick(fbrick: FlyingBrick) -> Brick:
    ranges: list[range] = []
    for c in range(3):
        endpoints = sorted([fbrick[0][c], fbrick[1][c]])
        ranges.append(range(endpoints[0], endpoints[1] + 1))
    return {(x, y, z) for x in ranges[0] for y in ranges[1] for z in ranges[2]}

pile: Grid = {}
bricks: list[Brick] = []
# for each brick, what bricks are directly below it?
below: dict[int, set[int]] = {}
above: dict[int, set[int]] = {}

# drop bricks into pile
for i, fbrick in enumerate(flying_bricks):
    # lower until supported in pile
    print(f"dropping {i} {fbrick}")
    brick = make_brick(fbrick)
    # don't drop it if it's at z=1
    supporters: set[int] = set()
    while fbrick[0][2] > 1:
        new_brick = {add_direction(pos, down) for pos in brick}
        collisions = new_brick & set(pile.keys())
        if collisions:
            print(f"{i} {fbrick} supported at {collisions}")
            for pos in collisions:
                supporter = pile[pos]
                supporters.add(supporter)
                above[supporter].add(i)
            break
        brick = new_brick
        fbrick = tuple(add_direction(pos, down) for pos in fbrick)
        # print(f"{i} dropping to {fbrick}")
    print(f"{i} landed at {fbrick}")
    for position in brick:
        if position in pile:
            raise ValueError("brick {i} intersecting {pile[position]} at {position}")
        pile[position] = i
    bricks.append(brick)
    below[i] = supporters
    above[i] = set()

for i, supporters in below.items():
    for j in supporters:
        if i not in above[j]:
            raise ValueError(f"{j} supports {i} but not in above")

for i, supporteds in above.items():
    for j in supporteds:
        if i not in below[j]:
            raise ValueError(f"{j} supported by {i} but not in below")

# for each brick, check supportiveness

free_bricks = 0
for i in range(len(bricks)):
    supported_bricks = above[i]
    removable = True
    for brick_no in supported_bricks:
        supporters = below[brick_no] - {i}
        if not supporters:
            # I don't think we need to worry about bricks on the ground
            removable = False
            break
    if removable:
        # print(f"brick {i} can be removed")
        free_bricks += 1
print(free_bricks)

# also find biggest chain reaction fall
best_chain = 0
best_chain_members: set[int] = set()
for i in range(len(bricks)):
    # only consider bricks on the ground
    if below[i]:
        continue
    chain_bricks: set[int] = {i}
    fallers: deque[int] = deque(above[i])
    while fallers:
        falling_brick = fallers.popleft()
        supporters = below[falling_brick] - chain_bricks
        if not supporters:
            # print(f"{falling_brick} not supported, falling")
            chain_bricks.add(falling_brick)
            for next_brick in above[falling_brick]:
                if next_brick not in fallers:
                    fallers.append(next_brick)
        else:
            print(f"{falling_brick} supported by {supporters}")

    for j, supports in below.items():
        if supports and j not in chain_bricks and supports < chain_bricks:
            raise ValueError(f"missed {j} somehow")
    print(f"{i}: {len(chain_bricks)}")
    if len(chain_bricks) > best_chain:
        best_chain = len(chain_bricks)
        best_chain_members = chain_bricks
print(best_chain)
