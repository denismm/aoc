#!/usr/bin/env python3
import sys

filename = sys.argv[1]
with open(filename, "r") as f:
    pad = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
    ]
    # NB: first coord is from top, second is from left
    location = [1, 1]
    directions = {
        "U": [-1, 0],
        "D": [1, 0],
        "L": [0, -1],
        "R": [0, 1],
    }
    output = []
    for line in f:
        # print(f"starting at {location}")
        for character in line.rstrip():
            direction = directions[character]
            for component in range(2):
                new_coord = location[component] + direction[component]
                if new_coord > 2 or new_coord < 0:
                    break
                else:
                    location[component] = new_coord
            # print (f"stepped {character} to {location}")
        output.append(str(pad[location[0]][location[1]]))
    print("".join(output))
