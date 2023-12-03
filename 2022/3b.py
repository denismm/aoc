#!/usr/bin/env python3
import sys


def item_priority(item: str) -> int:
    if "a" <= item <= "z":
        return 1 + ord(item) - ord("a")
    elif "A" <= item <= "Z":
        return 27 + ord(item) - ord("A")
    else:
        raise ValueError(f"invalid item {item}")


filename = sys.argv[1]
with open(filename, "r") as f:
    total_priority: int = 0
    elf_group: list[set[str]] = []
    for line in f:
        rucksack: str = line.rstrip()
        elf_group.append(set(rucksack))
        if len(elf_group) == 3:
            shared = elf_group[0] & elf_group[1] & elf_group[2]
            if len(shared) != 1:
                raise ValueError(f"non-single intersection: {shared}")
            item: str = shared.pop()
            priority: int = item_priority(item)
            print(f"{item} {priority}")
            total_priority += priority
            elf_group.clear()
    if len(elf_group) > 0:
        raise ValueError(f"incomplete elf group: {elf_group}")
    print(total_priority)
