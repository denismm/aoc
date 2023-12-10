#!/usr/bin/env python3
import sys
from positions import Position, Direction, add_direction, direction_for_symbol, get_direction

pipe_map: dict[Position, tuple[str, set[Position]]] = {}
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
character_for_dirs: dict[tuple[Direction, ...], str] = {
    tuple(sorted(v)): k for k, v in dirs_for_character.items()
}
filename = sys.argv[1]
start_location: Position = (-1, -1)
with open(filename, 'r') as f:
    for j, line in enumerate(f):
        for i, character in enumerate(line):
            if character in dir_chars_for_character:
                pos = (i, j)
                links = {add_direction(pos, direction) for direction in dirs_for_character[character]}
                pipe_map[pos] = (character, links)
                if character == 'S':
                    start_location = pos

if start_location == (-1, -1):
    raise ValueError("no start")

# clean broken start links
start_links = pipe_map[start_location][1]
start_directions: set[Direction] = set()
for link in list(start_links):
    if start_location not in pipe_map.get(link, ('.', set()))[1]:
        start_links.remove(link)
    else:
        start_directions.add(get_direction(start_location, link))
pipe_map[start_location] = (character_for_dirs[tuple(sorted(start_directions))], start_links)

# walk both ways, marking loop members
in_loop: set[Position] = {start_location}
steps = 1
last_positions = [start_location, start_location]
next_positions = list(pipe_map[start_location][1])
in_loop.update(next_positions)
if len(next_positions) != 2:
    raise ValueError(f"invalid map start: {next_positions}")
while next_positions[0] != next_positions[1]:
    for i in range(2):
        step_options = [p for p in pipe_map[next_positions[i]][1] if p != last_positions[i]]
        if len(step_options) != 1:
            raise ValueError(f"fork at {next_positions[i]}")
        last_positions[i] = next_positions[i]
        next_positions[i] = step_options[0]
    steps += 1
    in_loop.update(next_positions)

max_coord = max([max(position) for position in pipe_map.keys()])
# diagonal rasters doing in/out coloring
enclosed_total = 0
for k in range(-max_coord, max_coord + 1):
    inside: bool = False
    for i in range(0, max_coord + 1):
        position = (i, i + k)
        if position in in_loop:
            character = pipe_map[position][0]
            if character in '|-FJ':
                inside = not inside
        elif inside:
            enclosed_total += 1

print(f"steps to farthest point: {steps}")
print(f"enclosed_total: {enclosed_total}")
