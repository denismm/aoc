#!/usr/bin/env python3
import sys
from io import StringIO
from collections import defaultdict
from positions import (
    Position,
    StrGrid,
    add_direction,
    read_char_grid,
)

filename = sys.argv[1]

levels = 2

codes: list[str] = []
with open(filename, "r") as f:
    for line in f:
        codes.append(line.rstrip())

keypad_strings = ["789\n456\n123\n.0A\n", ".^A\n<v>\n"]
keypads: list[StrGrid] = [read_char_grid(StringIO(kps))[2] for kps in keypad_strings]
dapyeks: list[dict[str, Position]] = [{v: k for k, v in kp.items()} for kp in keypads]

best_transition: dict[int, dict[tuple[str, str], list[str]]] = defaultdict(dict)

def presses_for_transition(level: int, start: str, end: str) -> list[str]:
    key = (start, end)
    if key in best_transition[level]:
        return best_transition[level][key]
    if level == 0:
        kpi = 0
    else:
        kpi = 1
    start_pos = dapyeks[kpi][start]
    end_pos = dapyeks[kpi][end]
    h_distance = end_pos[0] - start_pos[0]
    v_distance = end_pos[1] - start_pos[1]
    moves: list[str] = []
    if h_distance != 0:
        if h_distance > 0:
            moves.append(">" * h_distance)
        else:
            moves.append("<" * -h_distance)
    if v_distance != 0:
        if v_distance > 0:
            moves.append("v" * v_distance)
        else:
            moves.append("^" * -v_distance)
    options: list[str] = []
    if len(moves) == 1:
        options = moves
    else:
        if add_direction(start_pos, (h_distance, 0)) in keypads[kpi]:
            options.append(''.join(moves))
        if add_direction(start_pos, (0, v_distance)) in keypads[kpi]:
            options.append(''.join(reversed(moves)))
    transitions = [ t + 'A' for t in options]
    if level < levels:
        transitions = [presses_for_sequence(level + 1, t) for t in transitions]
    best_len = min([len(t) for t in transitions])
    transitions = [t for t in transitions if len(t) == best_len]
    best_transition[level][key] = transitions
    return transitions

def presses_for_sequence(level: int, sequence: str) -> str:
    presses: list[str] = []
    for (start, end) in zip("A" + sequence, sequence):
        possible_presses = presses_for_transition(level, start, end)
        if len(set([len(p) for p in possible_presses])) > 1:
            raise ValueError(f"too many options: {possible_presses}")
        presses.append(presses_for_transition(level, start, end)[0])
    return "".join(presses)

total_complexity = 0
for code in codes:
    presses = presses_for_sequence(0, code)
    complexity = int(code[:-1]) * len(presses)
    print(code, len(presses), complexity, presses)
    total_complexity += complexity
print(total_complexity)