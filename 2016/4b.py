#!/usr/bin/env python3
import sys
import re
import collections

room_parser = re.compile(r"([a-z-]+)-(\d+)\[([a-z]{5})\]")

a_ord = ord("a")


def rot_letter(letter, n):
    if letter == "-":
        return " "
    else:
        id = ord(letter) - a_ord
        return chr(a_ord + (id + n) % 26)


filename = sys.argv[1]
with open(filename, "r") as f:
    valid_id_sum = 0
    for line in f:
        match = room_parser.match(line)
        (name, id, checksum) = match.groups()
        letter_count = collections.defaultdict(lambda: 0)
        for x in name:
            if x != "-":
                letter_count[x] += 1
        letters = sorted(letter_count.keys(), key=lambda x: (-1 * letter_count[x], x))
        correct_checksum = "".join(letters[:5])
        if checksum == correct_checksum:
            rotation = int(id) % 26
            realname = "".join([rot_letter(x, rotation) for x in name])
            if "north" in realname:
                print(realname, id)
