#!/usr/bin/env python3
import sys

filename = sys.argv[1]

with open(filename, 'r') as f:
    maze = [int(line.rstrip()) for line in f]

current_location = 0

steps = 0
while current_location < len(maze):
    last_location = current_location
    steps += 1
    current_location += maze[current_location]
    maze[last_location] += 1
    # print(maze)

print(steps)
