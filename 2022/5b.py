#!/usr/bin/env python3
import sys
import re
from typing import Pattern

crate_pattern: Pattern[str] = re.compile(r"\[(.)\]\s")
instruction_pattern: Pattern[str] = re.compile(
    r"move (\d+) from (\d+) to (\d+)")

filename = sys.argv[1]
with open(filename, "r") as f:
    stacks: list[list[str]] = []
    mode: str = "stacks"
    for line in f:
        if mode == "stacks":
            if line.startswith(" 1 "):
                expected_base = " ".join([f" {i + 1} "
                    for i in range(len(stacks))])
                if line.startswith(expected_base):
                    stacks = [list(reversed(x)) for x in stacks]
                    mode = "blank"
                    continue
                else:
                    raise ValueError(
                        "wrong base,"
                        f" {line.rstrip()} instead of {expected_base}"
                    )
            columns = len(line) // 4
            for i in range(columns):
                if len(stacks) <= i:
                    stacks.append([])
                section = line[4 * i : 4 * (i + 1)]
                m = crate_pattern.match(section)
                if m:
                    stacks[i].append(m.group(1))
        elif mode == "blank":
            if re.match(r"\s*$", line):
                mode = "instructions"
            else:
                raise ValueError(f"blank line not blank: {line}")
        elif mode == "instructions":
            m = instruction_pattern.match(line)
            if m:
                quantity: int
                source: int
                dest: int
                (quantity, source, dest) = [int(x) for x in m.groups()]
                source -= 1
                dest -= 1
                stacks[dest].extend(stacks[source][-quantity:])
                stacks[source] = stacks[source][:-quantity]
            else:
                raise ValueError(f"bad instructions: {line}")
    print("".join([stack[-1] for stack in stacks]))
