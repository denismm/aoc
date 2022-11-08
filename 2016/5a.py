#!/usr/bin/env python3
import sys
import hashlib
door_id = sys.argv[1]

i = 0
password = []
preamble = '00000'
while len(password) < 8:
    candidate = door_id + str(i)
    hash = hashlib.md5(candidate.encode()).hexdigest()
    if hash.startswith(preamble):
        password.append(hash[5])
        print(f"password {''.join(password)} found at {i}")
    i += 1
