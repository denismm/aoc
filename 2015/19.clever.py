#!/usr/bin/env python3
import sys
from collections import defaultdict

filename = sys.argv[1]

destination: str = ""
replacements: dict[str, list[str]] = defaultdict(list)
atoms: set[str] = set()
with open(filename, "r") as f:
    for line in f:
        line = line.rstrip()
        if len(line):
            if " => " in line:
                source, dest = line.split(" => ")
                replacements[source].append(dest)
                # get atoms
                atoms.add(source)
                while len(dest):
                    if len(dest) > 1 and 'a' <= dest[1] <= 'z':
                        atom_len = 2
                    else:
                        atom_len = 1
                    atoms.add(dest[:atom_len])
                    dest = dest[atom_len:]
            else:
                destination = line


# find equivalency groups and punctuation

dest_for_source: dict[str, set[str]] = defaultdict(set)
source_for_dest: dict[str, set[str]] = defaultdict(set)

for source, dests in replacements.items():
    for full_dest in dests:
        dest = full_dest[0]
        dest_for_source[source].add(dest)
        source_for_dest[dest].add(source)

equivs: dict[str, set[str]] = {}

for mapping in [dest_for_source, source_for_dest]:
    for point, neighbors in mapping.items():
        if point not in equivs:
            equivs[point] = {point}
        for neighbor in neighbors:
            if neighbor not in equivs:
                equivs[neighbor] = {neighbor}
            # merge equivs
            if equivs[point] is not equivs[neighbor]:
                equivs[point] |= equivs[neighbor]
                equivs[neighbor] = equivs[point]
seen_equivs: list[set[str]] = []

for atom in sorted(atoms):
    # print(f"{dest_for_source[atom]!s:20}\t{atom}\t{source_for_dest[atom]}")
    if equivs[atom] not in seen_equivs:
        print(f"{atom}:\t{equivs[atom]}")
        seen_equivs.append(equivs[atom])

print(destination)
