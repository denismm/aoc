#!/usr/bin/env python3
import sys
from positions import read_char_grid, StrGrid, Position, add_direction, cardinal_directions
from dataclasses import dataclass
from typing import Iterable
from copy import deepcopy

walls: StrGrid
original_players: list['Player'] = []

def first(positions: Iterable[Position]) -> Position:
    sorted_positions = sorted(positions, key=lambda p: (p[1], p[0]))
    return sorted_positions[0]

@dataclass
class Player:
    pos: Position
    side: str           # G or E
    hp: int = 200

    def __lt__(self, other: 'Player') -> bool:
        return (self.pos[1], self.pos[0]) < (other.pos[1], other.pos[0])

    def __repr__(self) -> str:
        return f"{self.side}({self.hp} {self.pos})"

    def targets(self) -> set[Position]:
        options = [add_direction(self.pos, d) for d in cardinal_directions]
        return set([o for o in options if o not in walls])


filename = sys.argv[1]
grid_width: int = 0
grid_height: int = 0
with open(filename, 'r') as f:
    grid_width, grid_height, walls = read_char_grid(f)

for position, symbol in walls.items():
    if symbol in "GE":
        player = Player(position, symbol)
        original_players.append(player)

for position in [c.pos for c in original_players]:
    del walls[position]

def count_sides() -> set[str]:
    return set([c.side for c in players])

def choose_enemy(enemies: list[Player]) -> Player:
    # fewest hit points or reading order
    hp_min: int = min([e.hp for e in enemies if e.hp > 0])
    weaklings = [e for e in enemies if e.hp == hp_min]
    weaklings.sort()
    return weaklings[0]

def draw_maze() -> None:
    player_for_location: dict[Position, Player] = {c.pos: c for c in players }
    print(f"Strength {attack['E']} Round {round}: {len(players)} players")
    for j in range(grid_height):
        player_report: list[str] = []
        maze_report: str = ""
        for i in range(grid_width):
            test_pos: Position = (i, j)
            if test_pos in player_for_location:
                player = player_for_location[test_pos]
                maze_report += player.side
                player_report.append(f"{player.side}({player.hp})")
            elif test_pos in walls:
                maze_report += "#"
            else:
                maze_report += "."
        print(f"{maze_report}   {', '.join(player_report)}")

attack: dict[str, int] = {"G": 3, "E": 4}

elfcount = len([c for c in original_players if c.side == 'E'])

debug_maze: bool = False
debug_finale: bool = False
debug_decisions: bool = False

done = False
while not done:
    players: list[Player] = deepcopy(original_players)
    # print(players)
    round = 0
    early_exit: bool = False
    # print("Day 15\n")
    while len(count_sides()) > 1:
        players.sort()
        if debug_maze:
            draw_maze()
        for c in players:
            # skip dead players
            if c.hp <= 0:
                continue

            # recalculate board after each move
            enemy_locations: set[Position] = set()
            friend_locations: set[Position] = set()
            enemy_targets: set[Position] = set()
            for e in players:
                if e == c:
                    continue
                if e.hp <= 0:
                    continue
                if e.side == c.side:
                    friend_locations.add(e.pos)
                if e.side != c.side:
                    enemy_targets |= e.targets()
                    enemy_locations.add(e.pos)
            player_locations = enemy_locations | friend_locations
            if not enemy_locations:
                early_exit = True

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
                            if np in walls or np in steps_to_point or np in player_locations:
                                continue
                            steps_to_point[np] = steps
                            if np in enemy_targets:
                                possible_targets.add(np)
                            else:
                                new_frontier.add(np)
                    frontier = new_frontier
                if not possible_targets:
                    # no target, skip player
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
                if debug_decisions:
                    print(f"{round}: Step decision: {c.side} at {c.pos}, going to {best_step}")
                c.pos = best_step

            # attack if in melee
            if c.pos in enemy_targets:
                local_targets = c.targets() & enemy_locations
                local_enemies = [e for e in players if e.pos in local_targets]
                enemy: Player = choose_enemy(local_enemies)
                if debug_decisions:
                    print(f"{round}: {c.side} at {c.pos} attacking {enemy}")
                enemy.hp -= attack[c.side]
        round += 1
        players = [c for c in players if c.hp > 0]

    if early_exit:
        round -= 1
    if debug_finale:
        draw_maze()
    hp_sum: int = sum([c.hp for c in players])
    winner = players[0].side
    print(attack['E'], winner, round, hp_sum, round * hp_sum)
    if winner == 'E' and len(players) == elfcount:
        exit(0)
    attack['E'] += 1
