#!./bin/python3
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from Levenshtein import distance
from heapq import heappush, heappop, heapify

@dataclass(order=True)
class Molecule:
    priority: float
    steps: int = field(compare=False)
    name: str = field(compare=False)

class PriorityQueue:
    def __init__(self) -> None:
        self.entries: list[Molecule] = []
        self.finder: dict[str, Molecule] = {}

    def put(self, entry: Molecule) -> None:
        if entry.name in self.finder:
            return
        self.finder[entry.name] = entry
        heappush(self.entries, entry)

    def get(self) -> Molecule:
        entry: Molecule = heappop(self.entries)
        del self.finder[entry.name]
        return entry
        
filename = sys.argv[1]

destination: str = ""
origin: str = "e"
replacements: dict[str, list[str]] = defaultdict(list)
with open(filename, 'r') as f:
    for line in f:
        line = line.rstrip()
        if len(line):
            if ' => ' in line:
                source, dest = line.split(' => ')
                replacements[source].append(dest)
            else:
                destination = line

frontier: PriorityQueue = PriorityQueue()
frontier.put(Molecule(0.0, 0, origin))
seen: set[str] = {origin}

def next_options(start: str) -> set[str]:
    outputs: set[str] = set()
    for source, dests in replacements.items():
        # print (source)
        position = 0
        found = True
        while found:
            position = start.find(source, position)
            if position == -1:
                found = False
                break
            # print(f"found {source} at {position}")
            for dest in dests:
                output = start[:position] + start[position:].replace(source, dest, 1)
                # print (f"{dest}: adding {output}")
                if output not in seen:
                    outputs.add(output)
            position += 1
    return outputs

coefficient: float = 0.1
print (f"target is {destination}")
while frontier:
    current = frontier.get()
    # print(f"got {current=}")
    nexts = next_options(current.name)
    for next in nexts:
        # print(f"checking {next}")
        steps = current.steps + 1
        if next == destination:
            print (steps)
            exit(0)
        priority = current.steps + coefficient * distance(next, destination)
        # print(f"putting {priority}, {steps}, {next}")
        frontier.put(Molecule(priority, steps, next))
    seen |= nexts
