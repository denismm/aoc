#!/usr/bin/env python3
import sys
import hashlib
import re
from typing import NamedTuple, Optional

salt = sys.argv[1]

triplet_re = re.compile(r'(.)\1{2}')
quintet_re = re.compile(r'(.)\1{4}')

IndexCandidate = NamedTuple('IndexCandidate', [('index', int), ('character', str)])
triplet_candidates: set[IndexCandidate] = set()
approved_candidates: list[IndexCandidate] = []

def check_hash(salt: str, index: int) -> tuple[Optional[str], set[str]]:
    input = salt + str(index)
    hash = hashlib.md5(input.encode()).hexdigest()
    triplet: Optional[str] = None
    if (m := triplet_re.search(hash)):
        triplet = m.group(1)
    quints: set[str] = set(quintet_re.findall(hash))
    # if triplet or quints:
        # print(f"for {i} found {triplet} and {quints}")
    return (triplet, quints)

i = 0

while True:
    triplet, quints = check_hash(salt, i)
    for candidate in list(triplet_candidates):
        if candidate.character in quints:
            triplet_candidates.remove(candidate)
            approved_candidates.append(candidate)
            # print(f"approved {candidate} at index {i}")
        elif candidate.index + 1000 <= i:
            # print(f"removing {candidate} at {i}")
            triplet_candidates.remove(candidate)
    if triplet is not None:
        triplet_candidates.add(IndexCandidate(i, triplet))
        # print(f'adding {triplet} at {i}')
    i += 1
    if len(approved_candidates) >= 64:
        approved_candidates.sort(key=lambda c: c.index)
        possible_winner = approved_candidates[63]
        pending = [c for c in triplet_candidates if c.index < possible_winner.index]
        if len(pending) == 0:
            print(possible_winner)
            exit(0)

