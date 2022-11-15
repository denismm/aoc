#!/usr/bin/env python3
import sys
import re

filename = sys.argv[1]
section_re = re.compile(r"([a-z]*)(?:\[([a-z]*)\])?")


def get_aba(sequence):
    for i in range(len(sequence) - 2):
        (a, b, c) = sequence[i : i + 3]
        if a == c != b:
            yield (a, b)


with open(filename, "r") as f:
    ssl_count = 0
    for line in f:
        base_aba = set()
        hyper_bab = set()
        sections = section_re.findall(line.rstrip())
        for section in sections:
            (base, hyper) = section
            for aba in get_aba(base):
                base_aba.add(aba)
            for aba in get_aba(hyper):
                hyper_bab.add(tuple(reversed(aba)))
        ssl = base_aba & hyper_bab
        if ssl:
            ssl_count += 1
    print(ssl_count)
