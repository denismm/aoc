#!/usr/bin/env python3
import sys
import re

filename = sys.argv[1]

rect_re = re.compile(r"rect\s(\d+)x(\d+)$")
rotate_re = re.compile(r"rotate\s(\w+)\s(\w)=(\d+)\sby\s(\d+)$")
display_width = 50
display_height = 6
display = [[0] * display_width for _ in range(display_height)]
with open(filename, "r") as f:
    for line in f:
        m = rect_re.match(line)
        if m:
            width, height = m.groups()
            for x in range(int(width)):
                for y in range(int(height)):
                    display[y][x] = 1
        else:
            m = rotate_re.match(line)
            if m:
                (type, coord, id, angle) = m.groups()
                id = int(id)
                angle = int(angle)
                if coord == "x":
                    buffer = [display[y][id] for y in range(display_height)]
                    for y in range(display_height):
                        display[y][id] = buffer[(y - angle) % display_height]
                elif coord == "y":
                    buffer = [display[id][x] for x in range(display_width)]
                    for x in range(display_width):
                        display[id][x] = buffer[(x - angle) % display_width]
                else:
                    raise ValueError(f"bad coord: {coord}")
            else:
                raise ValueError(f"bad line: {line}")
pixel = [".", "#"]
count = 0
for row in display:
    print("".join([pixel[r] for r in row]))
    count += sum(row)
print(count)
