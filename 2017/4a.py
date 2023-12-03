#!/usr/bin/env python3
import sys

filename = sys.argv[1]

with open(filename, 'r') as f:
    valids = 0
    for line in f:
        passphrase_words = line.rstrip().split()
        password_set = set(passphrase_words)
        if len(password_set) == len(passphrase_words):
            valids += 1
    print(valids)
