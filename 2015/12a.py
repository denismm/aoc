#!/usr/bin/env python3
import sys
import json
from typing import Any

filename = sys.argv[1]

with open(filename, 'r') as f:
    data = json.loads(f.read())

def sum_numbers(key: list[Any], input: dict[str, Any] | list[Any] | int) -> int:
    total: int = 0
    if isinstance(input, int):
        return input
    if isinstance(input, dict):
        for k, v in sorted(input.items()):
            total += sum_numbers(key + [k], v)
    elif isinstance(input, list):
        for i, v in enumerate(input):
            total += sum_numbers(key + [i], v)
    return total

print(sum_numbers([], data))
