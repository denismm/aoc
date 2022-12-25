#!/usr/bin/env python3
import sys

filename = sys.argv[1]
digit_value = {k: i for i, k in enumerate("=-012", start=-2)}
value_digit = {v: k for k, v in digit_value.items()}

with open(filename, "r") as f:
    total = 0
    for line in f:
        value = 0
        number = line.rstrip()
        for place, digit in enumerate(reversed(number)):
            value += digit_value[digit] * 5**place
        # print(f"{number}\t{value}")
        total += value

output: list[str] = []
while (total != 0):
    positive_mod = total % 5
    balanced_mod = (positive_mod + 2) % 5 - 2
    total = (total - balanced_mod) // 5
    output.append(value_digit[balanced_mod])
print(''.join(reversed(output)))
