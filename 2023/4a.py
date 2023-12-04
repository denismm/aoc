#!/usr/bin/env python3
import sys

filename = sys.argv[1]

total_points = 0
with open(filename, 'r') as f:
    for line in f:
        card_num, rest = line.rstrip().split(':')
        winner_s, number_s = rest.split('|')
        winners = set([int(s) for s in winner_s.split()])
        numbers = [int(s) for s in number_s.split()]
        winning_numbers = [n for n in numbers if n in winners]
        if winning_numbers:
            total_points += 1 << (len(winning_numbers) - 1)

print(total_points)
