#!/usr/bin/env python3
import sys
import re

nice_rules = [ re.compile(rule) for rule in (r'[aeiou].*[aeiou].*[aeiou]', r'(.)\1')]
naughty_rules = [ re.compile(rule) for rule in (r'ab', r'cd', r'pq', r'xy')]

def is_nice(line: str) -> bool:
    for rule in naughty_rules:
        if rule.search(line):
            return False
    for rule in nice_rules:
        if not rule.search(line):
            return False
    return True


filename = sys.argv[1]
nice: int = 0
with open(filename, 'r') as f:
    for line in f:
        if is_nice(line):
            nice += 1
print(nice)
