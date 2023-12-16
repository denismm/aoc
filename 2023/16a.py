#!/usr/bin/env python3
import sys
from positions import Position, add_direction, cardinal_directions

filename = sys.argv[1]

Grid = dict[Position, str]
grid: Grid = {}

with open(filename, "r") as f:
    for j, line in enumerate(f):
        line = line.rstrip()
        width = len(line)
        for i, char in enumerate(line.rstrip()):
            grid[(i, j)] = char
    height = j+1

# position of beam + index into cardinal_directions
Ray = tuple[Position, int]

angle_map: dict[str, dict[int, int]] = {
    '\\': {0: 1, 1: 0, 2: 3, 3: 2},
    '/' : {0: 3, 1: 2, 2: 1, 3: 0},
}


def score_ray(input: Ray) -> int:
    frontier: set[Ray] = {input}
    seen_rays: set[Ray] = set()

    while (frontier):
        frontier -= seen_rays
        seen_rays |= frontier
        new_frontier: set[Ray] = set()
        for position, direction in frontier:
            new_directions: list[int] = []
            char = grid[position]
            # print(position, direction, char)
            if char == '.':
                new_directions = [direction]
            elif char == '|':
                if direction in (0, 2):
                    new_directions = [1, 3]
                else:
                    new_directions = [direction]
            elif char == '-':
                if direction in (1, 3):
                    new_directions = [0, 2]
                else:
                    new_directions = [direction]
            elif char in '\\/':
                # print(f"dealing with {char}, {direction}")
                new_directions = [angle_map[char][direction]]
                # print(f"got directions {new_directions}")
            else:
                raise ValueError(f"mysterious grid entry: {char}")
            # print(new_directions)
            for new_direction in new_directions:
                new_frontier.add((add_direction(position, cardinal_directions[new_direction]), new_direction))
        # print(new_frontier)
        frontier = { ray for ray in new_frontier if ray[0] in grid }
        # print(frontier)

    seen_positions = set( position for position, direction in seen_rays )
    return (len(seen_positions))

print("current score:", score_ray( ((0, 0), 0) ) )

starts: list[Ray] = []
for i in range(width):
    starts.append(((i, 0), 1))
    starts.append(((i, height - 1), 3))
for j in range(height):
    starts.append(((0, j), 0))
    starts.append(((width - 1, j), 2))

print("best score:", max([score_ray(ray) for ray in starts]))
