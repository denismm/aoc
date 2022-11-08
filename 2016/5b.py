#!/usr/bin/env python3
import sys
import hashlib

door_id = sys.argv[1]

i = 0
password = ["."] * 8
preamble = "00000"
found = 0
while found < 8:
    candidate = door_id + str(i)
    hash = hashlib.md5(candidate.encode()).hexdigest()
    if hash.startswith(preamble):
        position = hash[5]
        if position <= "7":
            position = int(position)
            if password[position] == ".":
                password[position] = hash[6]
                print(f"password {''.join(password)} found at {i}")
                found += 1
    i += 1
