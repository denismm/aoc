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

levels = int(sys.argv[2])

codes: list[str] = []
with open(filename, "r") as f:
    for line in f:
        codes.append(line.rstrip())

keypad_strings = ["789\n456\n123\n.0A\n", ".^A\n<v>\n"]
keypads: list[StrGrid] = [read_char_grid(StringIO(kps))[2] for kps in keypad_strings]
dapyeks: list[dict[str, Position]] = [{v: k for k, v in kp.items()} for kp in keypads]

best_transitions: dict[int, dict[tuple[str, str], int]] = defaultdict(dict)
best_bases: dict[tuple[str, str], list[str]] = {}

def presses_for_transition(level: int, start: str, end: str) -> int:
    key = (start, end)
    if key not in best_transitions[level]:
        # find base
        if key not in best_bases:
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
            best_bases[key] = [ t + 'A' for t in options]
        bases = best_bases[key]
        if level < levels:
            best_len = min([presses_for_sequence(level + 1, t) for t in bases])
            # print (f"minned {best_len}")
        else:
            best_len = min([len(t) for t in bases])
            # print (f"calculated {best_len}")
        best_transitions[level][key] = best_len
    return best_transitions[level][key]

best_presses: dict[tuple[int, str], int] = {}
def presses_for_sequence(level: int, sequence: str) -> int:
    key = (level, sequence)
    # print (f"looking up {key}")
    if key not in best_presses:
        # print(f"calculating {key}")
        presses: int = 0
        for (start, end) in zip("A" + sequence, sequence):
            presses += presses_for_transition(level, start, end)
        best_presses[key] = presses
    else:
        # print(f"found {key}: {best_presses[key]}")
        pass
    return best_presses[key]

total_complexity = 0
for code in codes:
    presses = presses_for_sequence(0, code)
    complexity = int(code[:-1]) * presses
    print(code, presses, complexity)
    total_complexity += complexity
print(total_complexity)
