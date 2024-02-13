#!/usr/bin/env python3
import sys

current: list[str] = list(sys.argv[1])

key_letters = 'abcdefghijklmnopqrstuvwxy'
next_letters = 'bcdefghjjkmmnppqrstuvwxyz'
next_letter: dict[str, str] = {k: v for k, v in zip(key_letters, next_letters)}

# increment, skipping ilo
def increment() -> None:
    place = -1
    done = False
    while not done:
        if current[place] < 'z':
            current[place] = next_letter[current[place]]
            done = True
        else:
            current[place] = 'a'
            place -= 1

# clear any ilo
for place in range(len(current)):
    if current[place] in 'ilo':
        current[place] = next_letter[current[place]]
        for i in range(place + 1, len(current)):
            current[i] = 'a'
        break

valid = False
while not valid:
    increment()
    # check for straight
    straight = False
    for i in range(len(current) - 3):
        if ord(current[i]) == ord(current[i+1]) - 1 == ord(current[i+2]) - 2:
            straight = True
            break
    if straight:
        # check for 2 pair
        pairs: set[str] = set()
        for i in range(len(current) - 1):
            if ord(current[i]) == ord(current[i+1]):
                pairs.add(current[i])
        if len(pairs) >= 2:
            valid = True
            print(''.join(current))
