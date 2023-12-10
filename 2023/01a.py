#!/usr/bin/env python3
import sys

filename = sys.argv[1]
total = 0
with open(filename, 'r') as f:
    for line in f:
        digits = [c for c in line if c.isdigit()]
        calibration_s = ''.join((digits[0], digits[-1]))
        total += int(calibration_s)
print(total)
