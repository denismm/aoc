#!/usr/bin/env python3
import sys
import re
from collections import defaultdict
from tqdm import tqdm
from typing import Optional

# based on analysis - other inputs might map this differently

element_grid: list[list[str]] = [
    "F  Ca P  Si".split(),
    "Al Th zz zz".split(),
    "Mg B  Ti zz".split(),
    "zz H  N  O ".split(),
]
substitutions: dict[str, str] = {}
caps = "UVWX"
lows = "abcd"
for i in range(4):
    for j in range(4):
        element = element_grid[i][j]
        if element == 'zz':
            continue
        substitutions[element] = caps[i] + lows[j]

substitutions['C'] = "*"
substitutions['Ar'] = ")"
substitutions['Rn'] = '('
substitutions['Y'] = '.'

terminals = ("(", ".", ")", "*")
starts = ("(", ".")
ends = (".", ")")
filling = [ atom for atom in substitutions.values() if atom not in terminals ]

def substitute(m: re.Match[str]) -> str:
    return substitutions[m.group(0)] + " "

element_re = re.compile(r'[A-Z][a-z]?')

replacements: dict[str, list[list[str]]] = defaultdict(list)
molecule: list[str] = []

def join(molecule: list[str]) -> str:
    return " ".join(molecule)

filename = sys.argv[1]
with open(filename, 'r') as f:
    for rawline in f:
        line = element_re.sub(substitute, rawline).rstrip()
        # now pull translated version into data structure
        if len(line):
            # note extra space coming from substitution
            if '  => ' in line:
                source, dest = line.split("  => ")
                fulldest = dest.split()
                replacements[source].append(fulldest)
            else:
                molecule = line.split()

for orig_atom, new_atom in substitutions.items():
    print(f"{orig_atom}:\t{new_atom} => { [ join(rep) for rep in replacements[new_atom]] }")

if len(sys.argv) > 2:
    submol_start = int(sys.argv[2])
    submol_end = int(sys.argv[3])
    molecule = molecule[submol_start:submol_end]

print(join(molecule))

# target type, start, post-end, atoms
Target = tuple[str, int, int, list[str]]

def find_zone(mol: list[str]) -> Optional[Target]:
    # Try to find smallest section of 2 or more atoms bound by terminals
    # that won't change.  Don't include start or end, if whole mol
    # is zone we want the "aa" options below
    # ok to have internal parens
    smallest: Optional[Target] = None

    for start in range(1, len(mol)):
        # start - 1 needs to be a start
        if mol[start - 1] in starts:
            paren_level = 0
            for end in range(start, len(mol) + 1):
                if end < len(mol) and mol[end] == '(':
                    paren_level += 1
                    continue
                if end == len(mol) or mol[end] in ends:
                    if paren_level == 0 and end - start < 2:
                        # this start is invalid
                        # print(f"early end: {join(mol[start:end + 1])}")
                        break
                    else:
                        if paren_level == 0:
                            if smallest and (smallest[2] - smallest[1]) <= (end - start):
                                # found a zone but it's too big
                                break
                            smallest = ("zone", start, end, mol[start:end])
                        else:
                            if end < len(mol) and mol[end] == ')':
                                paren_level -= 1
    return smallest

def find_targets(mol: list[str], start_from: int = 0, end_at: int = -1) -> list[Target]:
    """
    Each target is the type of rule,
    the start and post-end of the replaceable section,
    and the contents of the section.
    """
    if end_at == -1:
        end_at = len(mol)
    targets: list[Target] = []
    # (aa) or (aa. or .aa) or .aa.
    if False:
        for i in range(start_at, end_at - 3):
            if mol[i] in starts and mol[i + 3] in ends:
                if mol[i + 1] in filling and mol[i + 2] in filling:
                    targets.append( ("(aa)", i+1, i+3, mol[i + 1: i + 3]) )
    # aa - watch for changes to either
    for i in range(start_at, end_at - 1):
        if mol[i] in filling and mol[i + 1] in filling:
            targets.append( ("aa", i, i + 2, mol[i: i + 2]) )
    # a(b.c.d) - watch for changes to a
    for i in range(start_at, end_at - 3):
        if mol[i] in filling and mol[i + 1] == '(':
            j = i + 2
            while mol[j] in filling and mol[j + 1] == '.':
                j += 2
            if mol[j + 1] == ')':
                targets.append( ("a(a.a)", i, j + 2, mol[i: j + 2]) )
    return targets


State = tuple[int, list[str]]   # steps and molecule
frontier: list[State] = [ (0, molecule) ]
seen: set[tuple[str, ...]] = { tuple(molecule) }
# should be no way to reach same state with different step count

def apply_change(molecule: list[str], source: str, target_struct: Target) -> list[str]:
    rule_time, start, end, target = target_struct
    new_molecule = list(molecule)
    new_molecule[start : end] = [source]
    if target[0][0] != source[0]:
        raise ValueError(f"Bad replacement! {join(target)} => {source}")
    # print(f"{start}: {join(target)} => {source} : {join(new_molecule)}")
    return new_molecule

def check_target(target_struct: Target) -> tuple[ str, list[str] ]:
    rule_type, start, end, target = target_struct
    sources: list[str] = []
    futures = 0
    for source, destinations in replacements.items():
        for destination in destinations:
            if destination == target:
                sources.append(source)
            elif rule_type == 'aa' and '(' not in destination:
                # either one could change
                if (destination[0][1], destination[1][0]) == (target[0][1], target[1][0]):
                    # print(f"{start}: {join(target)}: future match with  {join(destination)} => {source}")
                    # this means anything else we find just goes in possibilities
                    futures += 1
            elif rule_type == 'a(a.a)' and '(' in destination:
                if destination[0][-1] == target[0][-1]:
                    futures += 1
    if len(sources) != 1:
        # print(f"can't replace {join(target)}: {sources=}")
        for source in sources:
            if target_struct[3][0][0] != source[0]:
                raise ValueError(f"Bad replacement! {join(target_struct[3])} => {source}")
            possibilities.append( (target_struct, source) )
    # we have one change but might it not be the true change
    if futures:
        # print(f"multiple future options for {join(target)}")
        possibilities.append( (target_struct, sources[0]) )
    return ('wrong', [])

while frontier:
    new_frontier: list[State] = []
    if False:
        f_iter = frontier
    else:
        f_iter = tqdm(frontier)
    for (steps, molecule) in f_iter:
        for i, atom in enumerate(molecule):
            if atom in filling and len(atom) != 2:
                raise ValueError(f"Bad atom at {i}: {atom}")
        certain = False
        possibilities: list[tuple[Target, str]] = []
        # find a replaceable sequence
        zone: Optional[Target] = find_zone(molecule)
        if zone:
            zone_type, start_at, end_at, zone_atoms = zone
            # print(f"constraining to {join(zone_atoms)} at {start_at}:{end_at} of {len(molecule)} <{join(molecule[start_at - 1:end_at + 1])}>")
        else:
            start_at = 0
            end_at = -1
        targets = find_targets(molecule, start_at, end_at)
        # figure out correct replacement
        if targets:
            # break out of this if we find one that definitely fits
            for target_struct in targets:
                # answer, options = check_target(target_struct)
                rule_type, start, end, target = target_struct
                sources: list[str] = []
                futures = 0
                for source, destinations in replacements.items():
                    for destination in destinations:
                        # add the correct match
                        if destination == target:
                            sources.append(source)
                        # note future matches for aa
                        elif rule_type == 'aa' and '(' not in destination:
                            # either one could change
                            if (destination[0][1], destination[1][0]) == (target[0][1], target[1][0]):
                                # print(f"{start}: {join(target)}: future match with  {join(destination)} => {source}")
                                # this means anything else we find just goes in possibilities
                                futures += 1
                        # note future matches for a(a.a)
                        elif rule_type == 'a(a.a)' and '(' in destination:
                            if destination[0][-1] == target[0][-1]:
                                futures += 1
                if len(sources) != 1:
                    if len(sources) > 1:
                        raise(f"found multiple matches for {join(target)}: {sources=}")
                    # no sources here, move on to next target
                    continue

                # we have one change but might it not be the true change
                # keep looking for options
                if futures:
                    # print(f"multiple future options for {join(target)}")
                    possibilities.append( (target_struct, sources[0]) )
                    continue

                # this one works, replace and proceed
                new_molecule = apply_change(molecule, sources[0], target_struct)
                certain = True
                break
        if certain:
            # we found a match that definitely works
            if tuple(new_molecule) not in seen:
                new_frontier.append( (steps + 1, new_molecule) )
                seen.add(tuple(new_molecule))
        else:
            if False and end_at - start_at > len(molecule) / 2:
                print(join(molecule))
                print(len(possibilities))
                exit(0)
            # if we got here we have possibilities
            if len(possibilities) > 10 and False:
                print(f"adding {len(possibilities)}, constrained to {join(zone_atoms)} at {start_at}:{end_at} of {len(molecule)} <{join(molecule[start_at - 1:end_at + 1])}>")
            for possibility in possibilities:
                target_struct, source = possibility
                new_molecule = apply_change(molecule, source, target_struct)
                if tuple(new_molecule) not in seen:
                    new_frontier.append( (steps + 1, new_molecule) )
                    seen.add(tuple(new_molecule))
    if not new_frontier:
        print("finals")
        for state in frontier:
            print(f"{state[0]} : {join(state[1])}")
        exit(0)
    frontier = new_frontier
    if frontier:
        print(f"{len(frontier)=} {frontier[0][0]}")
