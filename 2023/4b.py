#!/usr/bin/env python3
import sys
from collections import defaultdict

filename = sys.argv[1]

total_cards = 0
card_counts: dict[int, int] = defaultdict(lambda: 1)
with open(filename, 'r') as f:
    for i, line in enumerate(f):
        multiplier = card_counts[i]
        total_cards += multiplier
        card_num, rest = line.rstrip().split(':')
        winner_s, number_s = rest.split('|')
        winners = set([int(s) for s in winner_s.split()])
        numbers = [int(s) for s in number_s.split()]
        winning_numbers = [n for n in numbers if n in winners]
        if winning_numbers:
            for di in range(len(winning_numbers)):
                card_counts[1 + i + di] += multiplier

print(total_cards)
