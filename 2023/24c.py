#!/usr/bin/env python3
import sys
from positions import Position, Direction, get_direction, scale_direction, add_direction, FloatDirection
from math import sqrt
from typing import NamedTuple
from itertools import combinations, product

filename = sys.argv[1]

Stone = NamedTuple('Stone', [
    ('pos', Position), ('dir', Direction),
])
stones: list[Stone] = []

with open(filename, "r") as f:
    for line in f:
        pos_s, dir_s = line.split('@')
        pos = tuple(int(x) for x in pos_s.split(', '))
        dir = tuple(int(x) for x in dir_s.split(', '))
        stones.append(Stone(pos, dir))

# if we draw all the stone paths out, and stand at the
# correct point to throw the rock from, all the paths should intersect
# in a single point in our vision along our target.
# This also means that any parallel lines need to look like a single
# line from our perspective, so we're on the plane defined by those points.
# Sadly there are no parallel lines.

# let's find a colinear point on four lines through refining an approximation
# I _know_ the order is 0, 3, 2, 1
# from looking at the scad file
# so just add _those_.
# but divide by the farthest distance? no :(
if stones[0].pos[0] > 100000:
    current_increment = 10 ** 11
    # start with close results from a different method
    # I've been re-filling results from this same script in a few cycles
    current_estimates = [177443247580, 403663893515, 673879272412, 1008195171796]
    point_order = [1, 2, 3, 0]
else:
    current_increment = 10 ** 0
    current_estimates = [0, 0, 0, 0]
    point_order = [1, 2, 0, 3]

interesting_stones = [stones[i] for i in point_order]

def distance_for_timestamps(timestamps: tuple[int, ...]) -> float:
    points = [
        add_direction(
            stone.pos,
            scale_direction( stone.dir, timestamp)
        )
        for stone, timestamp in zip(interesting_stones, timestamps)
    ]
    # print(timestamps, points)

    # order is now correct
    # let's try distance of 1 and 2 from line 03.

    axis_vec = get_direction(points[0], points[3])
    axis_len = sqrt(sum([a*a for a in axis_vec]))
    unit_dir: FloatDirection = tuple((a / axis_len) for a in axis_vec)
    distance_sum = 0.0
    # print(f"{axis_vec=} {axis_len=} {unit_dir=}")
    for point in points[1:3]:
        point_vector = get_direction(points[0], point)
        t = sum([a * b for a, b in zip(point_vector, unit_dir)])
        projection_point = tuple(b + t * d for b, d in zip(points[0], unit_dir))
        projection_vec = tuple((a - b) for a, b in zip(projection_point, point))
        sublen = sqrt(sum([a*a for a in projection_vec]))
        # print(f"{point_vector=} {t=} {projection_point=} {projection_vec=} {sublen=}")
        distance_sum += sublen
    # print(distance_sum)
    return distance_sum

while current_increment > 0:
    best_timestamps: tuple[int, ...] = ()
    best_distances: float = 0.0
    for timestamps in product(range(-9, 10), repeat=4):
        test_timestamps = tuple(
            current_estimate + timestamp * current_increment
            for timestamp, current_estimate in zip(timestamps, current_estimates)
        )
        distance_sum = distance_for_timestamps(test_timestamps)
        if best_timestamps == () or distance_sum < best_distances:
            best_timestamps = timestamps
            best_distances = distance_sum
    print(best_timestamps, best_distances)
    for i in range(4):
        current_estimates[i] += current_increment * best_timestamps[i]
    current_increment //= 10
    if best_distances == 0:
        break
    print(current_estimates)

# for some of these, this is clearly wrong
# but let's try each combination
def check_pair(timestamps: tuple[int, int], stone_choices: tuple[int, int]) -> None:
    collision_points: list[Position] = []
    chosen_stones = [stones[i] for i in stone_choices]
    for (stone, t) in zip(chosen_stones, timestamps):
        point = add_direction(stone.pos, scale_direction(stone.dir, t))
        collision_points.append(point)
    point_difference: Direction = get_direction(*collision_points)
    time_difference: int = timestamps[1] - timestamps[0]
    rock_dir_components: list[int] = []
    for x in point_difference:
        if x % time_difference:
            return
        rock_dir_components.append(x // time_difference)
    rock_dir = tuple(rock_dir_components)
    rock_pos = add_direction(collision_points[0], scale_direction(rock_dir, -timestamps[0]))
    rock = Stone(rock_pos, rock_dir)
    # print(f"for {timestamps}, got {rock_pos} {rock_dir}")
    # start at 0 as sanity check
    for i, stone in enumerate(stones[0:], start=0):
        # first dimension that doesn't give same answer is problem
        # some dimensions might be same dir, ok if same start
        stone_times: set[int] = set()
        for c in range(3):
            if stone.dir[c] == rock.dir[c]:
                if stone.pos[c] != rock.pos[c]:
                    if i > 2:
                        print(f"miss at {i}")
                    return
            else:
                coord_difference = rock.pos[c] - stone.pos[c]
                time_difference = stone.dir[c] - rock.dir[c]
                # ASSUMPTION: no non-integer hits expected
                if coord_difference % time_difference:
                    if i > 2:
                        print(f"non-integer hit at {i}")
                    return
                t = coord_difference // time_difference
                stone_times.add(t)
        if len(stone_times) > 1:
            if i > 2:
                print(f"miss at {i}")
            return
    print(f"rock {rock} hits all stones")
    print(f"result is {sum(rock.pos)}")
    exit(0)

for stone_choices in combinations(range(4), 2):
    true_stone_choices = tuple( point_order[i] for i in stone_choices)
    check_pair(tuple(current_estimates[i] for i in stone_choices), true_stone_choices)       # type: ignore [arg-type]
exit(0)
