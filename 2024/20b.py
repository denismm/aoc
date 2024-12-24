#!/usr/bin/env python3
import sys
from tqdm import tqdm
from itertools import product
from collections import defaultdict
from positions import (
    Position,
    SetGrid,
    add_direction,
    read_char_grid,
    cardinal_directions,
    manhattan,
)

filename = sys.argv[1]
max_cheat = int(sys.argv[2])
min_save = int(sys.argv[3])

with open(filename, "r") as f:
    width, height, grid = read_char_grid(f)

start: Position = [k for k, v in grid.items() if v == "S"][0]
end: Position = [k for k, v in grid.items() if v == "E"][0]
walls: SetGrid = {k for k, v in grid.items() if v == "#"}

# Ranked clouds of distances from either end
def examine_maze(start: Position, end: Position) -> tuple[dict[int, set[Position]], int]:
    # fill in seen_distances and wall_distances, return best time
    # ignore external walls
    frontier: set[Position] = {start}
    seen: set[Position] = {start}
    distances: dict[int, set[Position]] = {0: frontier}
    steps: int = 0
    while frontier:
        steps += 1
        new_frontier: set[Position] = set()
        for location in frontier:
            for direction in cardinal_directions:
                step = add_direction(location, direction)
                if step in walls:
                    continue
                if step in seen:
                    continue
                seen.add(step)
                if step == end:
                    # we don't need any part of the last frontier
                    return distances, steps
                new_frontier.add(step)
        frontier = new_frontier
        distances[steps] = frontier
    raise ValueError("no route to end")

from_start, fair_time = examine_maze(start, end)
from_end, check_time = examine_maze(end, start)
if fair_time != check_time:
    raise ValueError(f"impossible maze: {fair_time} != {check_time}")

cheat_times: dict[int, set[tuple[Position, Position]]] = defaultdict(set)
start_time: int = 0
start_points: set[Position] = set()
end_time: int = 0
end_points: set[Position] = set()
start_point: Position
end_point: Position

print(len(from_start))
for starts in tqdm(from_start.items()):
    start_time, start_points = starts
    for ends in from_end.items():
        end_time, end_points = ends
        cheat_time = fair_time - (start_time + end_time)
        if cheat_time <= 0:
            continue
        for start_point, end_point in product(start_points, end_points):
            cheat_distance = manhattan(start_point, end_point)
            if cheat_distance > max_cheat:
                continue
            saved_time = cheat_time - cheat_distance
            if saved_time >= min_save:
                cheat_times[saved_time].add((start_point, end_point))

cheat_count = 0
for k in sorted(cheat_times.keys()):
    cheat_count += len(cheat_times[k])
    # print(len(cheat_times[k]), k)

print(cheat_count)
