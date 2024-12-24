#!/usr/bin/env python3
import sys
from tqdm import tqdm
from positions import (
    Position,
    SetGrid,
    add_direction,
    read_char_grid,
    print_set_grid,
    cardinal_directions,
)

filename = sys.argv[1]

with open(filename, "r") as f:
    width, height, grid = read_char_grid(f)

start: Position = [k for k, v in grid.items() if v == "S"][0]
end: Position = [k for k, v in grid.items() if v == "E"][0]
walls: SetGrid = {k for k, v in grid.items() if v == "#"}

# Dijkstra, keep all walls, store distances
wall_distances: dict[Position, int] = {}
seen_distances: dict[Position, int] = {start: 0}

def examine_maze() -> int:
    # fill in seen_distances and wall_distances, return best time
    # ignore external walls
    frontier: set[Position] = {start}
    steps: int = 0
    while frontier:
        steps += 1
        new_frontier: set[Position] = set()
        for location in frontier:
            for direction in cardinal_directions:
                step = add_direction(location, direction)
                if step in walls:
                    if step[0] in (0, width - 1) or step[1] in (0, height - 1):
                        continue
                    if step not in wall_distances:
                        wall_distances[step] = steps
                    continue
                if step in seen_distances:
                    continue
                if step == end:
                    return steps
                seen_distances[step] = steps
                new_frontier.add(step)
        frontier = new_frontier
    raise ValueError("no route to end")

fair_time = examine_maze()

cheat_times: dict[Position, int] = {}

def check_cheat(wall: Position, distance: int) -> int:
    # start from wall
    # don't go anywhere that wouldn't be an improvement on seen_distances
    # find solution if possible
    frontier: set[Position] = {wall}
    seen: set[Position] = set()
    steps: int = distance
    while frontier and steps < fair_time:
        # print (f"checking {frontier} at {steps}")
        steps += 1
        new_frontier: set[Position] = set()
        for location in frontier:
            for direction in cardinal_directions:
                step = add_direction(location, direction)
                if step in walls:
                    # print(f"{step} is a wall")
                    continue
                if step in seen:
                    # print(f"{step} is seen")
                    continue
                if step in seen_distances and seen_distances[step] <= steps:
                    # print (f"{step} at {steps} is not a shortcut for {seen_distances[step]}")
                    continue
                if step == end:
                    # print (f"{step} is the end")
                    return steps
                seen.add(step)
                new_frontier.add(step)
        frontier = new_frontier
    raise ValueError("no route to end")

for wall, distance in tqdm(wall_distances.items()):
    try:
        # print(f"{wall=} {distance=}")
        cheat_time = check_cheat(wall, distance)
        # print(f"{cheat_time=}")
        if cheat_time < fair_time:
            cheat_times[wall] = fair_time - cheat_time
    except ValueError as e:
        if str(e) == 'no route to end':
            continue
        raise

good_cheats: int = 0
for cheat_time in sorted(set(cheat_times.values())):
    if cheat_time >= 100:
        cheats = [k for k, v in cheat_times.items() if v == cheat_time]
        good_cheats += len(cheats)
    # print(len(cheats), cheat_time, cheats)

print(good_cheats)

# print(print_set_grid(width, height, walls))

if False:
    for y in range(height):
        for x in range(width):
            p = (x, y)
            o: str = ""
            if p in cheat_times:
                cheat_time = cheat_times[p]
                if cheat_time <= 9:
                    o = chr(ord('0') + cheat_time)
                elif cheat_time <= 42:
                    o = chr(ord('A') + cheat_time - 1)
                else:
                    o = "$"
            elif p in walls:
                o = "#"
            else:
                o = "."
            print(o, end="")
        print("")

