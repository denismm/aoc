#!/usr/bin/env python3
import sys
import re
from positions import Position, Direction, add_direction, scale_direction

filename = sys.argv[1]
token_re = re.compile(r'\D+')

totals: list[int] = [0, 0]
with open(filename, "r") as f:
    a_dir: Direction = (0, 0)
    b_dir: Direction = (0, 0)
    target: Position = (0, 0)
    for line in f:
        tokens = token_re.split(line)
        if len(tokens) < 3:
            continue
        vector = (int(tokens[1]), int(tokens[2]))
        if 'A' in line:
            a_dir = vector
        elif 'B' in line:
            b_dir = vector
        elif 'Prize' in line:
            base_target = vector

            for solution, offset in enumerate((0, 10000000000000)):
                target = add_direction(base_target, scale_direction((1, 1), offset))
                # algebra done on paper
                b_presses: int = round((target[0]/a_dir[0] - target[1]/a_dir[1]) / (b_dir[0]/a_dir[0] - b_dir[1]/a_dir[1]))

                a_presses: int = round((target[0] - b_presses * b_dir[0]) / a_dir[0])
                if add_direction(scale_direction(a_dir, a_presses), scale_direction(b_dir, b_presses)) == target:

                    # print(f"found solution for {target}: {a_presses=} {b_presses=}")
                    totals[solution] += round(a_presses) * 3 + round(b_presses)

print(totals)
