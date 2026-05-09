#!/usr/bin/env python3
import sys
from positions import Position, Direction, manhattan, scale_position, div_position, add_direction
from dataclasses import dataclass
from collections import defaultdict
from tqdm import tqdm

filename = sys.argv[1]

lol: tuple[int, ...] = (-1, 0, 1)
ten: tuple[int, ...] = tuple(range(10))
fudges: list[Direction] = [(dx, dy, dz) for dx in lol for dy in lol for dz in lol]
@dataclass(order=True, eq=True, frozen=True)
class Nanobot:
    radius: int
    pos: Position

    # in the current resolution, is this nanobot close enough to the test pos?
    def check_radius(self, test: Position, resolution: int) -> bool:
        print_debug = False
        # if div_position((9999, 0, 0), resolution) == test:
            # print_debug = True
        origin = div_position(self.pos, resolution)
        local_fudges = fudges
        if resolution == 1:
            local_fudges = [(0, 0, 0)]
        for f in local_fudges:
            check_origin = add_direction(origin, f)
            if print_debug:
                print(f"{self}: m({check_origin=} {test=}) = {manhattan(check_origin, test)} ({self.radius} // {resolution} == {self.radius // resolution})")
            if manhattan(check_origin, test) <= self.radius // resolution:
                if print_debug:
                    print(f"{resolution=} {self=} close to {test}")
                return True
        if print_debug:
            print(f"{resolution=} {self=} far from {test}")
        return False

nanobots: list[Nanobot] = []

max_size: int = 0
with open(filename, 'r') as f:
    for line in f:
        pos_s, rad_s = line.split()
        pos_s = pos_s.strip('pos=<>,')
        pos = tuple([int(s) for s in pos_s.split(',')])
        rad = int(rad_s.split('=')[-1])
        nanobots.append(Nanobot(rad, pos))
        local_max = max([abs(c) for c in pos])
        max_size = max(local_max, max_size)

start_resolution: int = 10 ** (len(str(max_size)))
cave: dict[int, dict[Position, set[int]]] = defaultdict(dict)
cave[start_resolution] = { p: set(range(len(nanobots))) for p in [(x, y, z) for x in lol for y in lol for z in lol]}

offsets: list[Direction] = [(dx, dy, dz) for dx in ten for dy in ten for dz in ten]
best_count: int = len(nanobots)
resolution = start_resolution
while resolution > 1 and best_count > 1:
    # get higher resolution list
    scan_list: list[Position] = []
    scan_list = [k for k, v in cave[resolution].items() if len(v) >= best_count]
    # print(f"{scan_list=}")
    # print(f"target: {div_position((9999,0,0), resolution)}")
    print(f"scanning {resolution=} {best_count=} {len(scan_list)=}")
    # print(f"{resolution=} {scan_list=}")
    new_resolution = resolution // 10
    # scan at this resolution
    for position in tqdm(scan_list):
        origin = scale_position(position, 10)
        # print(f"scanning {position} as {origin}")
        for offset in offsets:
            print_debug = False
            candidate = add_direction(origin, offset)
            if candidate not in cave[new_resolution]:
                # if div_position((9999, 0, 0), resolution) == candidate:
                    # print_debug = True
                    # print(f"{candidate=}")
                cave[new_resolution][candidate] = set()
                for n in cave[resolution][position]:
                    if print_debug:
                        print(f"checking {candidate} for nanobot {n}")
                    if nanobots[n].check_radius(candidate, new_resolution):
                        if print_debug:
                            print(f"adding {n} to {candidate}")
                        cave[new_resolution][candidate].add(n)
                if print_debug:
                    print(cave[new_resolution][candidate])
    new_best = max([len(v) for v in cave[new_resolution].values()])
    if False:
        for (position, seen) in cave[new_resolution].items():
            if seen:
                print(f"{position}: {seen}")

    # print(f"{new_best=}")
    # this may be greater than best_count but we keep best_count going down
    # calculate best
    if new_best >= best_count:
        resolution = new_resolution
    else:
        best_count -= 1
        resolution = start_resolution

print(f"done with {resolution=} {best_count=}")
if best_count < 2:
    print("no intersections found")
    exit(1)
answer_options = [k for k, v in cave[resolution].items() if len(v) == best_count]
# print(answer_options)

answer = min([sum(p) for p in answer_options])
print(answer)
print([p for p in answer_options if sum(p) == answer])
