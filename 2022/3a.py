#!/usr/bin/env python3
import sys

def item_priority(item:str) -> int:
    if 'a' <= item <= 'z':
        return 1 + ord(item) - ord('a')
    elif 'A' <= item <= 'Z':
        return 27 + ord(item) - ord('A')
    else:
        raise ValueError(f"invalid item {item}")

filename = sys.argv[1]
with open(filename, "r") as f:
    total_priority:int = 0
    for line in f:
        rucksack:str = line.rstrip()
        if len(rucksack) % 2 != 0:
            raise ValueError(f"unbalanced rucksack {rucksack}")
        compartment_size:int = len(rucksack) // 2
        left:set[str] = set(rucksack[:compartment_size])
        right:set[str] = set(rucksack[compartment_size:])
        both:set[str] = left & right
        if len(both) != 1:
            raise ValueError(f"non-single intersection: {both}")
        item:str = both.pop()
        priority:int = item_priority(item)
        print(f"{item} {priority}")
        total_priority += priority
    print(total_priority)
