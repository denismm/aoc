#!/usr/bin/env python3
from dataclasses import dataclass
from typing import Optional
from enum import StrEnum
from copy import deepcopy
from heapq import merge

@dataclass
class Player:
    hp: int
    damage: int
    armor: int
    mana: int

Spell = StrEnum("Spell", ["MagicMissile", "Drain", "Shield", "Poison", "Recharge"])

SpellList = list[Spell]

costs: dict[Spell, int] = {
    Spell.MagicMissile: 53,
    Spell.Drain: 73,
    Spell.Shield: 113,
    Spell.Poison: 173,
    Spell.Recharge: 229,
}

durations: dict[Spell, int] = {
    Spell.Shield: 6,
    Spell.Poison: 6,
    Spell.Recharge: 5,
}

Effects = dict[Spell, int]

@dataclass
class State:
    player: Player
    boss: Player
    effects: Effects
    spent: int = 0
    spells_so_far: Optional[list[Spell]] = None

    def clone(self) -> 'State':
        return deepcopy(self)

    def __lt__(self, other: "State") -> bool:
        return (self.spent, self.player.hp, self.boss.hp) < (other.spent, other.player.hp, other.boss.hp)

    def add_spell(self, spell: Spell) -> None:
        if self.spells_so_far is None:
            self.spells_so_far = []
        cost = costs[spell]
        self.spent += cost
        self.player.mana -= cost
        self.spells_so_far.append(spell)

PricedNextState = tuple[int, Spell, State]

class PlayerDeath(Exception):
    pass
class BossDeath(Exception):
    pass

def deathcheck(state: State) -> None:
    # print(state)
    if state.player.hp <= 0:
        raise PlayerDeath()
    if state.player.mana < 0:
        raise PlayerDeath()
    if state.boss.hp <= 0:
        raise BossDeath()

# note - all apply functions mutate state
def apply_spell( state: State, spell: Spell) -> None:
    state.add_spell(spell)
    if spell is Spell.MagicMissile:
        state.boss.hp -= 4
    elif spell is Spell.Drain:
        state.boss.hp -= 2
        state.player.hp += 2
    else:
        if spell in state.effects:
            raise PlayerDeath()
        state.effects[spell] = durations[spell]
    deathcheck(state)

def apply_effects( state: State ) -> None:
    for spell, timer in list(state.effects.items()):
        if spell is Spell.Shield:
            pass        # effect during boss turn
        elif spell is Spell.Poison:
            state.boss.hp -= 3
        elif spell is Spell.Recharge:
            state.player.mana += 101
        else:
            raise ValueError(f"how did we get a {spell} state?")
        state.effects[spell] -= 1
        if state.effects[spell] == 0:
            del state.effects[spell]
    deathcheck(state)

def event_loop(state: State, spell: Spell) -> Optional[bool]:
    try:
        # effects happen
        apply_effects(state)
        # player casts
        apply_spell(state, spell)
        # effects happen
        apply_effects(state)
        # boss hits
        damage = state.boss.damage
        if Spell.Shield in state.effects:
            damage -= 7
        state.player.hp -= damage
        deathcheck(state)
        return None
    except PlayerDeath:
        return False
    except BossDeath:
        return True

def combat(state: State, spell_list: SpellList) -> Optional[bool]:
    for spell in spell_list:
        result = event_loop(state, spell)
        if result is not None:
            return result
    return result

def solve_state(start_state: State, check_list: SpellList = []) -> int:
    current_stems: list[PricedNextState] = [
        (cost, spell, start_state.clone()) for spell, cost in costs.items()
    ]

    tries = 0
    threshold = 1
    while True:
        head: PricedNextState = current_stems.pop(0)
        spent, spell, state = head

        tries += 1
        if tries == threshold:
            print(f"# {tries=}, {spent=}, {len(current_stems)=}")
            threshold *= 10

        result = event_loop(state, spell)
        if check_list and state.spells_so_far and check_list[:len(state.spells_so_far)] == state.spells_so_far:
            print(state.spells_so_far, result)
        if result is True:
            print(f"success at try {tries}")
            return spent
        if result is False:
            # no further spells can save you
            continue
        new_stems: list[PricedNextState] = []
        for next_spell, cost in costs.items():
            new_stems.append((spent + cost, next_spell, state.clone()))
        current_stems = list(merge(current_stems, new_stems))


def tests() -> None:
    test_state = State(
        Player(10, 0, 0, 250),
        Player(13, 8, 0, 0),
        {}
    )
    spell_list: SpellList = [Spell.Poison, Spell.MagicMissile]
    backup = test_state.clone()

    print(combat(test_state, spell_list))
    print(test_state.spent)
    print(solve_state(backup, spell_list))

    test_state = State(
        Player(10, 0, 0, 250),
        Player(14, 8, 0, 0),
        {}
    )
    spell_list = [Spell.Recharge, Spell.Shield, Spell.Drain, Spell.Poison, Spell.MagicMissile]
    backup = test_state.clone()

    print(combat(test_state, spell_list))
    print(test_state.spent)
    print(solve_state(backup, spell_list))

# tests()
# exit(0)

input_state = State(
    Player(50, 0, 0, 500),
    Player(55, 8, 0, 0),    # from input
    {}
    )

print(solve_state(input_state))
