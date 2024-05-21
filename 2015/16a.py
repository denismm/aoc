#!/usr/bin/env python3
import sys

filename = sys.argv[1]

gift_info: dict[str, int] = {
    "children": 3,
    "cats": 7,
    "samoyeds": 2,
    "pomeranians": 3,
    "akitas": 0,
    "vizslas": 0,
    "goldfish": 5,
    "trees": 3,
    "cars": 2,
    "perfumes": 1,
}

with open(filename, "r") as f:
    for line in f:
        line = line.rstrip()
        sue, properties = line.split(": ", 1)
        match = True
        for property in properties.split(", "):
            category, num_s = property.split(": ")
            if int(num_s) != gift_info[category]:
                match = False
                break
        if match:
            print(sue)
