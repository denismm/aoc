#!/usr/bin/env python3
import sys

choice_value: dict[str, int] = {
    "A": 1,
    "B": 2,
    "C": 3,
    "X": 1,
    "Y": 2,
    "Z": 3,
}


def move_score(move: str) -> int:
    elf, me = move.split(" ")
    elf_value = choice_value[elf]
    me_value = choice_value[me]
    score = me_value
    # (me_value - elf_value) % 3 = 0 for tie, 1 for win, 2 for loss
    # (me_value - elf_value + 1) % 3 = 1 for tie, 2 for win, 0 for loss
    score += 3 * ((me_value - elf_value + 1) % 3)
    return score


filename = sys.argv[1]
with open(filename, "r") as f:
    total_score: int = 0
    for line in f:
        total_score += move_score(line.rstrip())
    print(total_score)
