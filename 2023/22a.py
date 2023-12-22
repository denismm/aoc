#!/usr/bin/env python3
import sys
from positions import Position, add_direction
from pprint import pprint

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
support_for_brick: dict[int, set[int]] = {}
supported_by_brick: dict[int, set[int]] = {}

# drop bricks into pile
for i, fbrick in enumerate(flying_bricks):
    # lower until supported in pile
    brick = make_brick(fbrick)
    # don't drop it if it's at z=1
    supporters: set[int] = set()
    while fbrick[0][2] > 1:
        new_brick = {add_direction(pos, down) for pos in brick}
        collisions = new_brick & set(pile.keys())
        if collisions:
            for pos in collisions:
                supporter = pile[pos]
                supporters.add(supporter)
                supported_by_brick[supporter].add(i)
            break
        brick = new_brick
        fbrick = tuple(add_direction(pos, down) for pos in fbrick)
    for position in brick:
        pile[position] = i
    bricks.append(brick)
    support_for_brick[i] = supporters
    supported_by_brick[i] = set()

# for each brick, check supportiveness

free_bricks = 0
for i in range(len(bricks)):
    supported_bricks = supported_by_brick[i]
    removable = True
    for brick_no in supported_bricks:
        supporters = support_for_brick[brick_no] - {i}
        if not supporters:
            # I don't think we need to worry about bricks on the ground
            removable = False
            break
    if removable:
        # print(f"brick {i} can be removed")
        free_bricks += 1
print(free_bricks)
