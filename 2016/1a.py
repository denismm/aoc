#!/usr/bin/env python3
import sys
filename = sys.argv[1]
with open(filename, 'r') as f:
    for line in f:
        instructions = line.rstrip().split(', ')
        location = [0,0]
        direction = 0
        directions = ([0,1], [1,0], [0,-1], [-1,0])
        rotations = {'R':-1, 'L':1}
        for inst in instructions:
            direction += rotations[inst[0]]
            direction %= 4
            location[0] += directions[direction][0] * int(inst[1:])
            location[1] += directions[direction][1] * int(inst[1:])
        print (abs(location[0]) + abs(location[1]))
