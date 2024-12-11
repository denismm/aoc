#!/usr/bin/env python3
import sys
from tqdm import tqdm
filename = sys.argv[1]

with open(filename, "r") as f:
    stones: list[int] = [int(s) for s in f.read().split()]

blinks = 25

for _ in tqdm(range(blinks)):
    # rules:
    # 0 -> 1
    # even digits ABCD -> AB CD
    # *= 2024

    new_stones: list[int] = []
    addition: list[int] = []
    for stone in stones:
        str_stone = str(stone)
        if stone == 0:
            addition = [1]
        elif len(str_stone) % 2 == 0:
            halfway = len(str_stone) // 2
            addition = [ int(str_stone[:halfway]), int(str_stone[halfway:]) ]
        else:
            addition = [stone * 2024]
        new_stones += addition
    stones = new_stones
    # print(stones)
print(len(stones))
