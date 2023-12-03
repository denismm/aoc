#!/usr/bin/env python3
import sys

filename = sys.argv[1]

scanners: dict[int, int] = {}

with open(filename, 'r') as f:
    for line in f:
        (layer, range) = [int(x) for x in line.rstrip().split(': ')]
        scanners[layer] = range

def position_at_time(layer: int, time: int) -> int:
    if layer not in scanners:
        return -1
    range = scanners[layer]
    size = range - 1
    i = time % (2 * size)
    from_top = abs(size - i)
    position = size - from_top
    return position

def safe_start(start_time: int) -> bool:
    for layer in scanners.keys():
        if position_at_time(layer, layer + start_time) == 0:
            return False
    return True

start = 0
while True:
    if safe_start(start):
        print(start)
        exit(0)
    start += 1
