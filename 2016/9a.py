#!/usr/bin/env python3
import sys
import re

filename = sys.argv[1]

compression_re = re.compile(r'\((\d+)x(\d+)\)')
with open(filename, "r") as f:
    full_length = 0
    for line in f:
        input = re.sub(r'\s+', "", line)
        output = ""
        while len(input) > 0:
            m = compression_re.search(input)
            if m:
                (amount, rep) = m.groups()
                amount = int(amount)
                rep = int(rep)
                start = m.start()
                end = m.end()
                output += input[:start]
                repeton = input[end:end+amount]
                output += repeton * rep
                input = input[end+amount:]
            else:
                output += input
                input = ""
        full_length += len(output)
        print(output)
    print(full_length)
