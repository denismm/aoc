#!/usr/bin/env python3
import sys
from tqdm import tqdm
from collections import Counter
filename = sys.argv[1]
blinks = int(sys.argv[2])

# order doesn't matter so just track contents
stones: Counter[int] = Counter()

with open(filename, "r") as f:
    in_stones: list[int] = [int(s) for s in f.read().split()]
    stones = Counter(in_stones)


for _ in tqdm(range(blinks)):
    # rules:
    # 0 -> 1
    # even digits ABCD -> AB CD
    # *= 2024

    new_stones: Counter[int] = Counter()
    for stone, count in stones.items():
        str_stone = str(stone)
        if stone == 0:
            new_stones[1] += count
        elif len(str_stone) % 2 == 0:
            halfway = len(str_stone) // 2
            addition = [ str_stone[:halfway], str_stone[halfway:] ]
            for new_stone in addition:
                new_stones[int(new_stone)] += count
        else:
            new_stones[stone * 2024] += count
    stones = new_stones
    # print(stones)
print(sum(stones.values()))
