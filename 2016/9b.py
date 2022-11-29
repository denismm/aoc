#!/usr/bin/env python3
import sys
import re

filename = sys.argv[1]

compression_re = re.compile(r"\((\d+)x(\d+)\)")


def expand(input):
    out_length = 0
    while len(input) > 0:
        m = compression_re.search(input)
        if m:
            (amount, rep) = m.groups()
            amount = int(amount)
            rep = int(rep)
            start = m.start()
            end = m.end()
            # length of pre-code section
            out_length += start
            repeton = input[end : end + amount]
            repeton_length = expand(repeton)
            out_length += repeton_length * rep
            input = input[end + amount :]
        else:
            out_length += len(input)
            input = ""
    return out_length


with open(filename, "r") as f:
    full_length = 0
    for line in f:
        input = re.sub(r"\s+", "", line)
        out_length = expand(input)
        full_length += out_length
        print(out_length)
    print(full_length)
