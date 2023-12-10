#!/usr/bin/env python3
import sys
from positions import Position, Direction, add_direction, direction_for_symbol

pipe_map: dict[Position, set[Position]] = {}
dir_chars_for_character: dict[str, str] = {
    'S': 'v>^<',
    'F': 'v>',
    '7': 'v<',
    'J': '^<',
    'L': '>^',
    '|': 'v^',
    '-': '><',
}
dirs_for_character: dict[str, tuple[Direction, ...]] = {
    k: tuple(direction_for_symbol[d] for d in v)
    for k, v in dir_chars_for_character.items()
}
filename = sys.argv[1]
start_location: Position = (-1, -1)
with open(filename, 'r') as f:
    for j, line in enumerate(f):
        for i, character in enumerate(line):
            if character in dir_chars_for_character:
                pos = (i, j)
                links = {add_direction(pos, direction) for direction in dirs_for_character[character]}
                pipe_map[pos] = links
                if character == 'S':
                    start_location = pos

if pos == (-1, -1):
    raise ValueError("no start")
# clean broken links
for position, links in pipe_map.items():
    for link in list(links):
        if position not in pipe_map.get(link, set()):
            links.remove(link)

# walk both ways
steps = 1
last_positions = [start_location, start_location]
next_positions = list(pipe_map[start_location])
if len(next_positions) != 2:
    raise ValueError(f"invalid map start: {next_positions}")
while next_positions[0] != next_positions[1]:
    for i in range(2):
        step_options = [p for p in pipe_map[next_positions[i]] if p != last_positions[i]]
        if len(step_options) != 1:
            raise ValueError(f"fork at {next_positions[i]}")
        last_positions[i] = next_positions[i]
        next_positions[i] = step_options[0]
    steps += 1

print(steps)
