#!/usr/bin/env python3
import sys
filename = sys.argv[1]

gift_info: dict[str, int] = {
    'children': 3,
    'cats': 7,
    'samoyeds': 2,
    'pomeranians': 3,
    'akitas': 0,
    'vizslas': 0,
    'goldfish': 5,
    'trees': 3,
    'cars': 2,
    'perfumes': 1,
}

greater = { 'cats', 'trees' }
lesser = { 'pomeranians', 'goldfish'}

with open(filename, 'r') as f:
    for line in f:
        line = line.rstrip()
        sue, properties = line.split(': ', 1)
        match = True
        for property in properties.split(', '):
            category, num_s = property.split(': ')
            num = int(num_s)
            compare = gift_info[category]
            if category in greater:
                if num <= compare:
                    match = False
            elif category in lesser:
                if num >= compare:
                    match = False
            elif num != compare:
                match = False
            if not match:
                break
        if match:
            print(sue)
