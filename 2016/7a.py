#!/usr/bin/env python3
import sys
import re

filename = sys.argv[1]
section_re = re.compile(r"([a-z]*)(?:\[([a-z]*)\])?")
abba_re = re.compile(r"(.)(.)\2\1")


def is_abba(sequence):
    m = abba_re.search(sequence)
    return m and m.group(1) != m.group(2)


with open(filename, "r") as f:
    tls_count = 0
    for line in f:
        base_abba = False
        hyper_abba = False
        sections = section_re.findall(line.rstrip())
        for section in sections:
            (base, hyper) = section
            if is_abba(base):
                base_abba = True
            if is_abba(hyper):
                hyper_abba = True
        tls = base_abba and not hyper_abba
        if tls:
            tls_count += 1
    print(tls_count)
