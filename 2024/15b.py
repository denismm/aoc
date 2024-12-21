#!/usr/bin/env python3
import sys
from positions import Position, Direction, add_direction, read_char_grid, direction_for_symbol
from typing import Optional

filename = sys.argv[1]

transformation: dict[str, str] = {
    '#': '##',
    'O': '[]',
    '.': '..',
    '@': '@.',
}

instructions: str = ""
with open(filename, "r") as f:
    _, _, grid = read_char_grid(f, transformation=transformation)
    for line in f:
        instructions += line.rstrip()

robot: Position = [k for k, v in grid.items() if v == '@'][0]

boxes: set[Position] = {k for k, v in grid.items() if v == '['}

walls: set[Position] = {k for k, v in grid.items() if v == '#'}
# print(boxes)

# we no longer care about grid

def boxat(left: Position) -> Optional[Position]:
    # print(f"checking {left=}")
    if left in boxes:
        return left
    right = add_direction(left, (-1, 0))
    # print(f"checking {right=}")
    if right in boxes:
        return right
    return None

def pushing(point: Position, dir: Direction) -> Optional[set[Position]]:
    # return possibly-empty set of boxes pushed or None if wall hit
    step = add_direction(point, dir)
    if step in walls:
        # print(f"wall at {step}")
        return None
    direct_push = boxat(step)
    # print(f"direct is {direct_push}")
    if direct_push is None:
        # print(f"clear sailing at {point} {dir}")
        return set()
    push_boxes: set[Position] = {direct_push}
    push_points: set[Position] = set()
    if dir != (-1, 0):
        push_points.add(add_direction(direct_push, (1, 0)))
    if dir != (1, 0):
        push_points.add(direct_push)
    # print(f"{push_points=}")
    for p in push_points:
        result = pushing(p, dir)
        if result is None:
            # print(f"can't push {point} {dir} because of {p}")
            return None
        push_boxes |= result
    # print(f"pushing {len(push_boxes)} boxes")
    return push_boxes

for dir in instructions:
    # print(robot, dir)
    direction: Direction = direction_for_symbol[dir]

    # try to move
    push_boxes: Optional[set[Position]] = pushing(robot, direction)
    if push_boxes is None:
        continue
    # print(robot, dir, len(push_boxes))
    boxes -= push_boxes
    boxes |= {add_direction(b, direction) for b in push_boxes}

    # if this had been a wall, pushing would have returned None
    robot = add_direction(robot, direction)

gps_total = 0
for box in boxes:
    gps_total += (100 * box[1] + box[0])
print(gps_total)
