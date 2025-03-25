#!/usr/bin/env python3
import sys

filename = sys.argv[1]

State = set[int]
current_state: State = set()
# only store the true rules
Rule = frozenset[int]
rules: set[Rule] = set()

init_s = 'initial state: '

with open(filename, 'r') as f:
    for line in f:
        if line.startswith(init_s):
            state_s = line[len(init_s):-1]
            current_state = set([i for i, c in enumerate(state_s) if c == '#'])
        elif '=> #' in line:
            rule_s = line[:5]
            rule: Rule = frozenset([i - 2 for i, c in enumerate(rule_s) if c == '#'])
            rules.add(rule)

def neighborhood(state: State, center: int) -> Rule:
    neighbors: set[int] = set()
    for i in range(-2, 3):
        if center + i in state:
            neighbors.add(i)
    return frozenset(neighbors)

stop = False
i = 0
while not stop:
    next_state: State = set()
    for center in range(min(current_state) - 2, max(current_state) + 3):
        match = neighborhood(current_state, center)
        if match in rules:
            next_state.add(center)
    # check for similarity
    if len(next_state) == len(current_state):
        diffs = set([b - a for a, b in zip(sorted(current_state), sorted(next_state))])
        if len(diffs) == 1:
            print(f"diff is {diffs}, sum is {sum(current_state)}, len is {len(current_state)}, i is {i}")
            steps_left = 50000000000 - i
            current_answer = sum(current_state)
            drift = diffs.pop()
            final_answer = current_answer + drift * len(current_state) * steps_left
            print(final_answer)
            stop = True
    current_state = next_state
    i += 1
