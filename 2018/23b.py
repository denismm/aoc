#!/usr/bin/env python3
import sys
from positions import Position, Direction, manhattan, add_direction, scale_direction
from dataclasses import dataclass
from itertools import combinations
from typing import Optional

filename = sys.argv[1]

# order means we can sort to get the best radius
@dataclass(order=True, eq=True, frozen=True)
class Nanobot:
    radius: int
    pos: Position

nanobots: list[Nanobot] = []

with open(filename, 'r') as f:
    for line in f:
        pos_s, rad_s = line.split()
        pos_s = pos_s.strip('pos=<>,')
        pos = tuple([int(s) for s in pos_s.split(',')])
        rad = int(rad_s.split('=')[-1])
        nanobots.append(Nanobot(rad, pos))

BotCluster = frozenset[Nanobot]
# find overlaps
overlaps: dict[BotCluster, int] = {}

for a, b in combinations(nanobots, 2):
    distance = manhattan(a.pos, b.pos)
    overlap = 1 + a.radius + b.radius - distance
    if overlap > 0:
        overlaps[frozenset((a, b))] = overlap
# print(overlaps)
# find clusters
print(f'got {len(overlaps)} overlaps')
clusters: dict[int, set[BotCluster]] = {2: set(overlaps.keys())}
cluster_size = 2
while clusters[cluster_size]:
    next_cluster_size = cluster_size + 1
    clusters[next_cluster_size] = set()
    for cluster in clusters[cluster_size]:
        for target in nanobots:
            addable = True
            if target in cluster:
                continue
            for source in cluster:
                if frozenset((source, target)) not in overlaps:
                    addable = False
                    break
            if addable:
                clusters[next_cluster_size].add(frozenset(cluster | {target}))
    cluster_size = next_cluster_size
    print(cluster_size)

near_point: Optional[int] = None

directions: list[Direction] = [
    (0, 0, 1), (0, 0, -1),
    (0, 1, 0), (0, -1, 0),
    (1, 0, 0), (-1, 0, 0),
]

class NotInside(Exception):
    pass

for cluster in clusters[cluster_size - 1]:
    # find points in overlap
    combos = combinations(cluster, 2)
    cluster_overlaps: list[tuple[int, BotCluster]] = []
    for combo in combos:
        subcluster = frozenset(combo)
        cluster_overlaps.append((overlaps[subcluster], subcluster))
    seed = min(cluster_overlaps)
    source, target = list(seed[1])
    octant: list[int] = [0, 0, 0]
    zeroes = 0
    for c in range(3):
        dim_distance = target.pos[c] - source.pos[c]
        if dim_distance > 0:
            octant[c] = 1
        elif dim_distance < 0:
            octant[c] = -1
        else:
            zeroes += 1
    # point or points that should be in the overlap for these two bots
    ping: set[Position] = set()
    ping_dir: list[int]
    if zeroes == 2:
        # this should be in the overlap
        ping.add(add_direction(source.pos, scale_direction(tuple(octant), source.radius)))
    elif zeroes == 1:
        if octant[0] == 0:
            c = 1
            d = 2
        else:
            c = 0
            if octant[1] == 0:
                d = 2
            else:
                d = 1
        for x in range(source.radius + 1):
            y = source.radius - x
            ping_dir = [0, 0, 0]
            ping_dir[c] = x * octant[c]
            ping_dir[d] = y * octant[d]
            ping_point = add_direction(source.pos, tuple(ping_dir))
            if manhattan(ping_point, target.pos) <= target.radius:
                ping.add(ping_point)
    else:       # no zeroes
        for x in range(source.radius + 1):
            for y in range(1 + source.radius - x):
                z = source.radius - x - y
                ping_dir = [x * octant[0], y * octant[1], z * octant[2]]
                if manhattan(ping_point, target.pos) <= target.radius:
                    ping.add(ping_point)
    print(ping)
    # find full overlap for these two bots
    search_space: set[Position] = set()
    frontier: set[Position] = ping
    while frontier:
        search_space |= frontier
        new_frontier: set[Position] = set()
        for root in frontier:
            for dir in directions:
                leaf = add_direction(root, dir)
                if leaf in search_space:
                    continue
                if manhattan(source.pos, leaf) <= source.radius:
                    if manhattan(target.pos, leaf) <= target.radius:
                        new_frontier.add(leaf)
        frontier = new_frontier
    # print(search_space)
    solutions: list[Position] = []
    for point in search_space:
        try:
            for nanobot in cluster:
                if manhattan(nanobot.pos, point) > nanobot.radius:
                    raise NotInside()
            solutions.append(point)
        except NotInside:
            continue
    sums = [sum(point) for point in solutions]
    best = min(sums)
    if near_point is None or best < near_point:
        near_point = best
print(best)
