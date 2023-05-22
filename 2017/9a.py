#!/usr/bin/env python3
import sys
from enum import Enum

filename = sys.argv[1]

ScanMode = Enum('ScanMode', ['GROUP', 'GARBAGE'])

def analyze_line(line: str) -> tuple[int, int]:
    score = 0
    depth = 0
    mode = ScanMode.GROUP
    cancel = False
    garbage = 0
    # open group: add to depth
    # close group: add depth to score, decrease depth
    # modes:
    # group or garbage
    # cancel or not
    for character in line:
        if mode == ScanMode.GROUP:
            if character == '<':
                mode = ScanMode.GARBAGE
            elif character == '{':
                depth += 1
            elif character == '}':
                score += depth
                depth -= 1
            elif character == ',':
                pass    # don't care about commas
            else:
                raise ValueError(f"didn't expect {character} in group")
        else:   # GARBAGE mode
            if cancel:
                cancel = False
            elif character == '!':
                cancel = True
            elif character == '>':
                mode = ScanMode.GROUP
            else:
                garbage += 1
    if depth != 0:
        raise ValueError(f"group not closed: depth is {depth}")
    return garbage, score

with open(filename, 'r') as f:
    for line in f:
        garbage, score = analyze_line(line.rstrip())
        print(f"score is {score}, garbage is {garbage}")
