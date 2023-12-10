#!/usr/bin/env python3
import sys
import hashlib

door_id = sys.argv[1]

i = 0
preamble = "000000"
while True:
    candidate = door_id + str(i)
    hash = hashlib.md5(candidate.encode()).hexdigest()
    if hash.startswith(preamble):
        print(f"ok hash found at {i}")
        exit(0)
    i += 1
