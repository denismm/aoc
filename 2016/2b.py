#!/usr/bin/env python3
import sys
import copy

filename = sys.argv[1]
with open(filename, "r") as f:
    pad = [
        "XX1XX",
        "X234X",
        "56789",
        "XABCX",
        "XXDXX",
    ]
    # NB: first coord is from top, second is from left
    location = [2, 0]

    def key_for_loc(coordinates):
        return pad[coordinates[0]][coordinates[1]]

    directions = {
        "U": [-1, 0],
        "D": [1, 0],
        "L": [0, -1],
        "R": [0, 1],
    }
    output = []
    for line in f:
        # print(f"starting at {location} ({key_for_loc(location)})")
        for character in line.rstrip():
            # print(f"{location}:{character}")
            direction = directions[character]
            new_location = copy.copy(location)
            for component in range(2):
                new_coord = new_location[component] + direction[component]
                if new_coord > 4 or new_coord < 0:
                    # print(f"can't go {character}")
                    new_location = None
                    break
                else:
                    new_location[component] = new_coord
                    # print(f"half-step to {new_location}")
            if new_location is not None:
                if key_for_loc(new_location) != "X":
                    location = new_location
                    # print (f"stepped {character} to {location} ({key_for_loc(location)})")
                else:
                    # print (f"can't go to X")
                    pass
        # print(f"got {key_for_loc(location)} at  {location}")
        output.append(key_for_loc(location))
    print("".join(output))
