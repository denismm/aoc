#!/usr/bin/env python3
import sys
from positions import Position, Direction, get_direction, scale_direction, add_direction
from typing import NamedTuple
from itertools import permutations

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

# for each i,j, both > 0, i != j, starting small and getting bigger:
# pretend that the rock hits stone 0 at time i and 1 at time j
# figure out where the starting point and direction are
# check the other stones, bailing when we miss
# with 300 stones, if these two aren't more than hits 600
# then it'll be 360_000 checks, mostly algebra so shouldn't be long
# but no, t can be pretty large I think - all the coordinates are 15 digits
# so let's try every combination of stones so we find the first two

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

exp_tracker = 10
for i in range(2, 100000000000):
    for j in range(1, i):
        for stone_choices in permutations(range(len(stones)), 2):
            check_pair((i, j), stone_choices)   # type: ignore [arg-type]
    if i == exp_tracker:
        print( f"done with {i}")
        exp_tracker *= 10
