#!/usr/bin/env python3
import sys

ROCK_LIMIT = 2022
# remember that the first entry in the array is the _bottom_
BASE_ROCKS: list[bytes] = [
    bytes([15]),        # -
    bytes([2, 7, 2]),   # +
    bytes([7, 1, 1]),   # L
    bytes([1, 1, 1, 1]),        # |
    bytes([3, 3]),      # square
]

rocks: list[list[bytes]] = []
for base in BASE_ROCKS:
    positions = [base]
    while True:
        last = False
        candidate: list[int] = []
        for b in positions[-1]:
            if b >= 63:
                last = True
                break
            candidate.append(b << 1)
        if last:
            break
        positions.append(bytes(candidate))
    rocks.append(positions)

filename = sys.argv[1]
with open(filename, "r") as f:
    file_data = f.read()
jets: list[str] = [ c for c in file_data if c in '<>']

chamber = bytearray()

rock_count = 0
tick = 0
# this is all the positions for the current rock
current_rock: list[bytes] = []
elevation = 0
position = 0

def summon_rock() -> None:
    global current_rock
    global chamber
    global elevation
    global position
    current_rock = rocks[rock_count % len(rocks)]
    position = len(current_rock) - 3
    rock_height = len(current_rock[0])

    # chamber is only as long as needed between drops
    elevation = len(chamber) + 3
    chamber += b'\0' * (rock_height + 3)

def check_collision(position: int, elevation: int) -> bool:
    rock_bytes = current_rock[position]
    for i in range(len(rock_bytes)):
        if chamber[elevation + i] & rock_bytes[i]:
            return True
    return False

def shift_rock() -> int:
    jet = jets[tick % len(jets)]
    if jet == '<':
        next_position = position + 1
    else:
        next_position = position - 1
    if not 0 <= next_position < len(current_rock):
        return position
    if check_collision(next_position, elevation):
        return position
    return next_position

def stop_rock() -> None:
    global current_rock
    global rock_count
    rock_bytes = current_rock[position]
    for i in range(len(rock_bytes)):
        chamber[elevation + i] |= rock_bytes[i]
    current_rock = []
    rock_count += 1
    while chamber[-1] == 0:
        chamber.pop()

def drop_rock() -> None:
    global elevation
    new_elevation = elevation - 1
    if new_elevation < 0 or check_collision(position, new_elevation):
        stop_rock()
    else:
        elevation = new_elevation

while rock_count < ROCK_LIMIT:
    if current_rock == []:
        summon_rock()
    position = shift_rock()
    drop_rock()
    tick += 1
print(len(chamber))

def display() -> None:
    display_char = '.#'
    if current_rock == []:
        rock_bytes = b''
    else:
        rock_bytes = current_rock[position]
    for height in reversed(range(len(chamber))):
        row = chamber[height]
        rock_r = height - elevation
        if 0 <= rock_r < len(rock_bytes):
            row |= rock_bytes[rock_r]
        print( ''.join([display_char[(row & 2 ** i) // 2**i] for i in reversed(range(7))]))
