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
        seen = {tuple(location)}
        done = False
        for inst in instructions:
            direction += rotations[inst[0]]
            direction %= 4
            steps = int(inst[1:])
            for i in range(steps):
                location[0] += directions[direction][0]
                location[1] += directions[direction][1]
                if tuple(location) in seen:
                    print(abs(location[0]) + abs(location[1]))
                    done = True
                    break
                else:
                    seen.add(tuple(location))
            if done:
                break
        if not done:
            print("got lost")
