#!/usr/bin/env python3
import sys

digit_strings = {
    'one'  : 1,
    'two'  : 2,
    'three': 3,
    'four' : 4,
    'five' : 5,
    'six'  : 6,
    'seven': 7,
    'eight': 8,
    'nine' : 9,
}

filename = sys.argv[1]
total = 0
with open(filename, 'r') as f:
    for line in f:
        digits: list[int] = []
        for i in range(len(line)):
            if line[i].isdigit():
                digits.append(int(line[i]))
            else:
                for (k, v) in digit_strings.items():
                    if line[i:].startswith(k):
                        digits.append(v)
        calibration = digits[0] * 10 + digits[-1]
        total += calibration
print(total)
