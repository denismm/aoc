#!/usr/bin/env python3
import sys
import math

elf_count = int(sys.argv[1])

def find_winner(elf_count: int) -> int:
    elves = list(range(elf_count))
    player = 0
    while len(elves) > 1:
        position = elves.index(player)
        victim = (position + len(elves) // 2) % len(elves)
        del elves[victim]
        if victim > position:
            position += 1
        # otherwise it's moved along
        position = position % len(elves)
        player = elves[position]
    return player

def simple_winner(elf_count:int) -> int:
    elf_count -= 1
    ec_in_ternary = ternary(elf_count)
    biggest_three: int = 3 ** (math.floor(math.log(elf_count, 3)))
    if ec_in_ternary[0] == '2':
        return elf_count - (biggest_three * 3 - elf_count) + 1
    else:
        return (elf_count - biggest_three)

def ternary(value: int) -> str:
    output: list[str] = []
    while value > 0:
        output.append(str(value % 3))
        value //= 3
    return ''.join(reversed(output))

def test(all_counts):
    for i in range(4, all_counts + 1):
        winner = find_winner(i)
        easy_winner = simple_winner(i)
        print(i, ternary(i - 1), winner, easy_winner, ternary(winner), (i - 1) - winner, winner - easy_winner)

print(simple_winner(elf_count) + 1)
