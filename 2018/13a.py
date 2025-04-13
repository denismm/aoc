#!/usr/bin/env python3
import sys
from positions import read_char_grid, StrGrid, Position, Direction, direction_for_symbol, add_direction, direction_symbols, cardinal_directions
from dataclasses import dataclass

@dataclass
class Cart:
    pos: Position
    dir: Direction
    turns: int = 0
    live: bool = True

    def __lt__(self, other: 'Cart') -> bool:
        return (self.pos[1], self.pos[0]) < (other.pos[1], other.pos[0])

filename = sys.argv[1]

tracks: StrGrid

with open(filename, 'r') as f:
    _, _, tracks = read_char_grid(f)

carts: list[Cart] = []

under: dict[str, str] = {c: t for c, t in zip('>v<^', '-|-|')}

for position, symbol in tracks.items():
    if symbol in direction_symbols:
        cart = Cart(position, direction_for_symbol[symbol])
        carts.append(cart)
        tracks[position] = under[symbol]

ziagonal_turn_chars: dict[str, str] = {c: t for c, t in zip('>v<^', '^<v>')}
niagonal_turn_chars: dict[str, str] = {c: t for c, t in zip('>v<^', 'v>^<')}
turn_for_corner_chars: dict[str, dict[str, str]] = {
    '/': ziagonal_turn_chars,
    '\\': niagonal_turn_chars,
}
turn_for_corner: dict[str, dict[Direction, Direction]] = {}
for corner, mapping in turn_for_corner_chars.items():
    dir_mapping: dict[Direction, Direction] = {}
    for d_in, d_out in mapping.items():
        dir_mapping[direction_for_symbol[d_in]] = direction_for_symbol[d_out]
    turn_for_corner[corner] = dir_mapping

ticks = 0
first_crash: bool = False
while len(carts) > 1:
    # put carts in order
    carts.sort()
    new_carts: list[Cart] = []
    while carts:
        cart = carts.pop(0)
        if not cart.live:
            continue
        cart.pos = add_direction(cart.pos, cart.dir)
        # check for collisions
        for other in carts + new_carts:
            if cart.pos == other.pos:
                if not first_crash:
                    print(f"tick {ticks}: collision at {str(cart.pos).replace(' ', '')}")
                    first_crash = True
                # don't add it, kill the other one
                cart.live = False
                if other in new_carts:
                    new_carts.remove(other)
                else:
                    other.live = False
                break
        if not cart.live:
            continue
        track = tracks[cart.pos]
        if track in turn_for_corner:
            cart.dir = turn_for_corner[track][cart.dir]
        elif track == '+':
            turn = cart.turns - 1
            if turn != 0:
                dir_pos = cardinal_directions.index(cart.dir)
                next_dir_pos = (dir_pos + turn) % 4
                cart.dir = cardinal_directions[next_dir_pos]
            cart.turns += 1
            cart.turns %= 3
        new_carts.append(cart)
    carts = new_carts
    ticks += 1
print(f"tick {ticks}: one cart left at {str(carts[0].pos).replace(' ', '')}")
