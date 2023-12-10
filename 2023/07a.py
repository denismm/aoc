#!/usr/bin/env python3
import sys
from typing import NamedTuple
from collections import defaultdict

Score = tuple[int, ...]

Hand = NamedTuple('Hand', [('cards', str), ('bid', int), ('score', Score)])

filename = sys.argv[1]

hands: list[Hand] = []

rank_for_face = {
    'T': 10,
    'J': 11,
    'Q': 12,
    'K': 13,
    'A': 14,
}
for i in range(1, 10):
    rank_for_face[str(i)] = i

hand_scores: dict[str, int] = {
    'HC': 0,    # 5 ranks, [1 1 1 1 1]
    '1P': 1,    # 4 ranks, [1 1 1 2]
    '2P': 2,    # 3 ranks, [1 2 2]
    '3K': 3,    # 3 ranks, [1 1 3]
    'FH': 4,    # 2 ranks, [2 3]
    '4K': 5,    # 2 ranks, [1 4]
    '5K': 6,    # 1 rank,  [5]
}

hand_type_for_ranks_and_biggest_stack: dict[int, dict[int, str]] = {
    1: { 5: '5K'},
    2: {
        4: '4K',
        3: 'FH',
    },
    3: {
        3: '3K',
        2: '2P',
    },
    4: { 2: '1P' },
    5: { 1: 'HC' },
}

def find_score(cards: str) -> Score:
    count_for_rank: dict[int, int] = defaultdict(lambda: 0)
    ranks = tuple(rank_for_face[face] for face in cards)
    for rank in ranks:
        count_for_rank[rank] += 1
    hand_type: str = ""
    rank_count = len(count_for_rank.keys())
    rank_sizes = sorted(count_for_rank.values())
    try:
        hand_type = hand_type_for_ranks_and_biggest_stack[rank_count][rank_sizes[-1]]
    except KeyError:
        raise ValueError(f"can't score {cards}: {rank_count=} {rank_sizes=}")
    return (hand_scores[hand_type], *ranks)

with open(filename, 'r') as f:
    for line in f:
        cards, bid_s = line.split()
        score = find_score(cards)
        hands.append(Hand(cards, int(bid_s), score))
hands.sort(key=lambda x: x.score)

total_winnings = 0
for i, hand in enumerate(hands):
    total_winnings += hand.bid * (i + 1)
print(total_winnings)
