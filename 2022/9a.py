#!/usr/bin/env python3
import sys

direction_map: dict[str, tuple[int, int]] = {
    "R": (1, 0),
    "U": (0, 1),
    "L": (-1, 0),
    "D": (0, -1),
}
ROPE_LENGTH = 10


def distance(a: list[int], b: list[int]) -> int:
    return max([abs(ac - bc) for ac, bc in zip(a, b)])


filename = sys.argv[1]
with open(filename, "r") as f:
    knot_loc: list[list[int]] = [[0, 0] for _ in range(ROPE_LENGTH)]
    tail_places: set[tuple[int, int]] = set()

    def log_loc(location: list[int]) -> None:
        tail_places.add((location[0], location[1]))

    log_loc(knot_loc[-1])
    for line in f:
        (direction, count_string) = line.split()
        count = int(count_string)
        step = direction_map[direction]
        for _ in range(count):
            knot_loc[0] = [l + d for l, d in zip(knot_loc[0], step)]
            for i in range(ROPE_LENGTH - 1):
                front = knot_loc[i]
                back = knot_loc[i + 1]
                if distance(front, back) > 1:
                    for c in range(2):
                        separation = front[c] - back[c]
                        if separation:
                            back[c] += separation // abs(separation)
            log_loc(knot_loc[-1])
    print(len(tail_places))
