#!/usr/bin/env python3
import sys
import re
from collections import defaultdict
from tqdm import tqdm

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

def join(molecule: list[str]) -> str:
    return " ".join(molecule)

print(join(molecule))

Target = tuple[str, int, int, list[str]]

def find_targets(mol: list[str]) -> list[Target]:
    """
    Each target is the type of rule,
    the start and post-end of the replaceable section,
    and the contents of the section.
    """
    targets: list[Target] = []
    # (aa) or (aa. or .aa) or .aa.
    for i in range(len(mol) - 3):
        if mol[i] in starts and mol[i + 3] in ends:
            if mol[i + 1] in filling and mol[i + 2] in filling:
                targets.append( ("(aa)", i+1, i+3, mol[i + 1: i + 3]) )
    # aa - watch for changes to either
    for i in range(len(mol) - 1):
        if mol[i] in filling and mol[i + 1] in filling:
            targets.append( ("aa", i, i + 2, mol[i: i + 2]) )
    # a(b.c.d) - watch for changes to a
    for i in range(len(mol) - 3):
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
    return new_molecule

while frontier:
    new_frontier: list[State] = []
    for (steps, molecule) in tqdm(frontier):
        for i, atom in enumerate(molecule):
            if atom in filling and len(atom) != 2:
                raise ValueError(f"Bad atom at {i}: {atom}")
        certain = False
        possibilities: list[tuple[Target, str]] = []
        # find a replaceable sequence
        targets = find_targets(molecule)
        # figure out correct replacement
        if targets:
            for target_struct in targets:
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
                                futures += 1
                        elif rule_type == 'a(a.a)' and '(' in destination:
                            if start > 0 and molecule[start - 1] not in starts:
                                if destination[0][-1] == target[0][-1]:
                                    futures += 1
                if len(sources) != 1:
                    # print(f"can't replace {join(target)}: {sources=}")
                    for source in sources:
                        possibilities.append( (target_struct, source) )
                    continue
                if futures:
                    # print(f"multiple future options for {join(target)}")
                    possibilities.append( (target_struct, source[0]) )
                    continue

                # this one works, replace and proceed
                new_molecule = apply_change(molecule, sources[0], target_struct)
                certain = True
                if tuple(new_molecule) not in seen:
                    new_frontier.append( (steps + 1, new_molecule) )
                    seen.add(tuple(new_molecule))
                # print(f"{steps}: {start}: {join(target)} => {sources[0]} : {join(new_molecule)}")
                break
        if not certain:
            # if we got here we have possibilities
            for possibility in possibilities:
                target_struct, source = possibility
                new_molecule = apply_change(molecule, source, target_struct)
                if tuple(new_molecule) not in seen:
                    new_frontier.append( (steps + 1, new_molecule) )
                    seen.add(tuple(new_molecule))
    frontier = new_frontier
    print(f"{len(frontier)=} {frontier[0][0]}")

# print(steps)
# print(join(molecule))
