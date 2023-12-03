#!/usr/bin/env python3
import sys
import json
from typing import Union, Optional
from functools import cmp_to_key

Packet = Union[int, list["Packet"]]


def check_correct(a: Packet, b: Packet) -> Optional[bool]:
    if isinstance(a, int):
        if isinstance(b, int):
            if a == b:
                return None
            return a < b
        else:
            return check_correct([a], b)
    else:
        if isinstance(b, int):
            return check_correct(a, [b])
        else:
            for i in range(min([len(a), len(b)])):
                correct = check_correct(a[i], b[i])
                if correct is not None:
                    return correct
            if len(a) != len(b):
                return len(a) < len(b)
            return None


def packet_cmp(a: Packet, b: Packet) -> int:
    transform: dict[Optional[bool], int] = {True: -1, None: 0, False: 1}
    return transform[check_correct(a, b)]


filename = sys.argv[1]
with open(filename, "r") as f:
    correct_count: int = 0
    i: int = 1
    pair: list[Packet] = []
    all_packets: list[Packet] = []

    def check_pair() -> None:
        global i
        global correct_count
        if len(pair) != 2:
            raise ValueError("invalid packet set: {pair}")
        if check_correct(*pair):
            correct_count += i
        i += 1
        pair.clear()

    for line in f:
        data = line.rstrip()
        if len(data):
            this_packet: Packet = json.loads(data)
            pair.append(this_packet)
            all_packets.append(this_packet)
        else:
            check_pair()
    if len(pair):
        check_pair()
    print(correct_count)

    dividers = [ [[2]], [[6]] ]
    all_packets += dividers # type: ignore[arg-type]
    sorted_packets = sorted(all_packets, key=cmp_to_key(packet_cmp))
    div_indices = [ sorted_packets.index(div) + 1 for div in dividers ] # type: ignore[arg-type]
    print(div_indices[0] * div_indices[1])
