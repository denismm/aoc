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

total_severity: int = 0

for layer in scanners.keys():
    if position_at_time(layer, layer) == 0:
        severity = layer * scanners[layer]
        print(f"caught at layer {layer}, adding {severity}")
        total_severity += severity

print( total_severity )
