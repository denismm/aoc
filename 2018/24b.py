#!/usr/bin/env python3
import sys
from dataclasses import dataclass
import re
from typing import Optional
from copy import deepcopy

@dataclass()
class Group:
    side: str           # Infection or Immune System
    number: int
    size: int
    hp: int
    issues: dict[str, int]    # multiplier for damage = 2 or 0
    attack_hp: int
    attack_type: str
    initiative: int
    target: Optional['Group'] = None

    def __repr__(self) -> str:
        return f"{self.side} {self.number} {self.size}"

    def effective_power(self) -> int:
        return self.size * self.attack_hp

    def alive(self) -> bool:
        return self.size > 0

    def selection_key(self) -> tuple[int, int]:
        # decreasing order of effective power, higher initiative first
        return (-1 * self.effective_power(), -1 * self.initiative)

    def attacking_key(self) -> int:
        # in decreasing order of initiative
        return -1 * self.initiative

    def damage(self, target: 'Group') -> int:
        ap = self.effective_power()
        ap *= target.issues.get(self.attack_type, 1)
        return ap

issue_magnitude: dict[str, int] = {'immune': 0, 'weak': 2}

groups: list[Group] = []

group_re = re.compile(r'(\d+) units each with (\d+) hit points (?:\(([^()]+)\) )?with an attack that does (\d+) (\w+) damage at initiative (\d+)')

filename = sys.argv[1]
with open(filename, 'r') as f:
    current_side = ""
    number = 0
    for line in f:
        line = line.rstrip()
        if ':' in line:
            current_side = line.split(':')[0]
            number = 0
            continue
        if len(line) == 0:
            continue
        if m := group_re.match(line):
            number += 1
            size = int(m.group(1))
            hp = int(m.group(2))
            issue_s = m.group(3)
            attack_hp = int(m.group(4))
            attack_type = m.group(5)
            initiative = int(m.group(6))
            issues: dict[str, int] = {}
            if issue_s:
                for issue_section in issue_s.split('; '):
                    issue, issue_types = issue_section.split(' to ')
                    magnitude = issue_magnitude[issue]
                    for issue_type in issue_types.split(', '):
                        issues[issue_type] = magnitude
            groups.append(Group(current_side, number, size, hp, issues, attack_hp, attack_type, initiative))
        else:
            raise ValueError(f"couldn't parse {line}")

for g in groups:
    print(f"{g} {g.attack_hp} {g.issues}")

# original setup complete

def try_boost( original_groups: list[Group], boost: int ) -> str:        # winning side
    groups = deepcopy(original_groups)
    for g in groups:
        if g.side == 'Immune System':
            g.attack_hp += boost
    while True:
        # selection
        groups.sort(key=Group.selection_key)
        targetted: list[Group] = []
        for attacker in groups:
            attacker.target = None
            raw_targets: list[Group] = [g for g in groups if g not in targetted and g.side != attacker.side]
            targets: list[tuple[int, Group]] = [(attacker.damage(g), g) for g in raw_targets]
            # attack where most damage goes, or largest effective power, or highest initiative
            targets.sort(key=lambda t: (t[0], t[1].effective_power(), t[1].initiative))
            if False:
                for t in targets:
                    print(f"{attacker}: {t}")
            if targets:
                target = targets[-1]
                if target[0] > 0:
                    attacker.target = target[1]
                    targetted.append(target[1])

        # print()
        # combat!
        peace = True
        groups.sort(key=Group.attacking_key)
        for attacker in groups:
            if attacker.alive() and attacker.target is not None:
                damage = attacker.damage(attacker.target)
                kills = min(damage // attacker.target.hp, attacker.target.size)
                # print(f"{attacker} vs {attacker.target}: {kills}")
                if kills > 0:
                    peace = False
                attacker.target.size -= kills

        groups = [g for g in groups if g.alive()]
        # print([g.size for g in groups])

        sides = { g.side for g in groups }
        # print()
        if peace:
            print(f"{boost}: peace with {groups}")
            return "Stalemate"
        if len(sides) <= 1:
            print(f"{boost}: win for {sides}", end="")
            print(sum([g.size for g in groups]))
            return sides.pop()

boost: int = -1
winner: str = "None"
while winner != "Immune System":
    boost += 1
    winner = try_boost( groups, boost)

print( boost )
