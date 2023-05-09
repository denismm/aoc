#!/usr/bin/env python3
import sys
from enum import Enum

filename = sys.argv[1]

ScanMode = Enum('ScanMode', ['GROUP', 'GARBAGE'])

def analyze_line(line: str) -> int:
    score = 0
    depth = 0
    mode = ScanMode.GROUP
    cancel = False
    # open group: add to depth
    # close group: add depth to score, decrease depth
    # modes:
    # group or garbage
    # cancel or not
    for character in line:
        if cancel:
            cancel = False
        elif character == '!':
            cancel = True
        elif mode == ScanMode.GROUP:
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
            if character == '>':
                mode = ScanMode.GROUP
    if depth != 0:
        raise ValueError(f"group not closed: depth is {depth}")
    if cancel:
        raise ValueError("mid-cancel at end")
    return score

with open(filename, 'r') as f:
    for line in f:
        score = analyze_line(line.rstrip())
        print(score)
