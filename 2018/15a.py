#!/usr/bin/env python3
import sys
from positions import read_char_grid, StrGrid, Position, Direction, add_direction, cardinal_directions
from dataclasses import dataclass
from typing import Iterable

walls: StrGrid
combatants: list['Combatant'] = []

def first(positions: Iterable[Position]) -> Position:
    sorted_positions = sorted(positions, key=lambda p: (p[1], p[0]))
    return sorted_positions[0]

@dataclass
class Combatant:
    pos: Position
    side: str           # G or E
    attack: int = 3
    hp: int = 200

    def __lt__(self, other: 'Combatant') -> bool:
        return (self.pos[1], self.pos[0]) < (other.pos[1], other.pos[0])

    def targets(self) -> set[Position]:
        options = [add_direction(self.pos, d) for d in cardinal_directions]
        return set([o for o in options if o not in walls])


filename = sys.argv[1]
with open(filename, 'r') as f:
    _, _, walls = read_char_grid(f)

for position, symbol in walls.items():
    if symbol in "GE":
        combatant = Combatant(position, symbol)
        combatants.append(combatant)

for position in [c.pos for c in combatants]:
    del walls[position]

def count_sides() -> set[str]:
    return set([c.side for c in combatants])

round = 0
while len(count_sides()) > 1:
    combatants.sort()
    for c in combatants:
        # skip dead combatants
        if c.hp <= 0:
            continue

        # recalculate board after each move
        enemy_locations: set[Position] = set()
        friend_locations: set[Position] = set()
        enemy_targets: set[Position] = set()
        for e in combatants:
            if e == c:
                continue
            if e.hp <= 0:
                continue
            if e.side == c.side:
                friend_locations.add(e.pos)
            if e.side != c.side:
                enemy_targets |= e.targets()
                enemy_locations.add(e.pos)
        combatant_locations = enemy_locations | friend_locations

        # move if not in melee
        if c.pos not in enemy_targets:
            steps_to_point: dict[Position, int] = {c.pos: 0}
            frontier: set[Position] = {c.pos}
            possible_targets: set[Position] = set()
            steps: int = 0
            while frontier and not possible_targets:
                # Dijkstra out until enemy or no paths
                new_frontier: set[Position] = set()
                steps += 1
                for p in frontier:
                    for d in cardinal_directions:
                        np = add_direction(p, d)
                        if np in walls or np in steps_to_point:
                            continue
                        steps_to_point[np] = steps
                        if np in enemy_targets:
                            possible_targets.add(np)
                        else:
                            new_frontier.add(np)
                frontier = new_frontier
            if not possible_targets:
                # no target, skip combatant
                continue
            # find best target
            target = first(possible_targets)
            # find best path
            back_frontier: set[Position] = {target}
            steps = steps_to_point[target]
            while steps > 1:
                new_frontier = set()
                for p in back_frontier:
                    for d in cardinal_directions:
                        np = add_direction(p, d)
                        if steps_to_point.get(np, steps) == steps - 1:
                            new_frontier.add(np)
                steps -= 1
                back_frontier = new_frontier
            best_step = first(back_frontier)
            print(c.side, best_step)
            c.pos = best_step

        # attack if in melee
        if c.pos in enemy_targets:
            local_targets = c.targets() & enemy_locations
            chosen_target = first(local_targets)
            enemy: Combatant = [e for e in combatants if e.pos == chosen_target][0]
            print(round, c.side, enemy)
            enemy.hp -= c.attack
    round += 1
    combatants = [c for c in combatants if c.hp > 0]
    print(round, combatants)
