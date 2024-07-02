#!/usr/bin/env python3
from dataclasses import dataclass
from typing import Optional, Iterable
from enum import StrEnum
from copy import deepcopy

@dataclass
class Player:
    hp: int
    damage: int
    armor: int
    mana: int

Spell = StrEnum("Spell", ["MagicMissile", "Drain", "Shield", "Poison", "Recharge"])

SpellList = list[Spell]
PricedSpellList = tuple[int, SpellList]

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

    def clone(self) -> 'State':
        return deepcopy(self)

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
    state.player.mana -= costs[spell]
    state.spent += costs[spell]
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

def all_spell_lists() -> Iterable[PricedSpellList]:
    current_stems: list[PricedSpellList] = [
        (cost, [spell]) for spell, cost in costs.items()
    ]
    current_stems.sort()

    while True:
        head: PricedSpellList = current_stems.pop(0)
        for spell, cost in costs.items():
            current_stems.append((head[0] + cost, head[1] + [spell]))
        current_stems.sort()
        yield head

def test_iterator() -> None:
    for i, priced_spell_list in zip(range(20), all_spell_lists()):
        print(priced_spell_list)

# test_iterator()

def solve_state(start_state: State) -> None:
    tries = 0
    threshold = 1
    for priced_spell_list in all_spell_lists():
        cost, spell_list = priced_spell_list
        state = start_state.clone()
        if combat(state, spell_list):
            print(cost, state.spent)
            return
        tries += 1
        if tries == threshold:
            print(f"# {tries=}, {cost=}, {len(spell_list)=}")
            threshold *= 10

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
    solve_state(backup)

    test_state = State(
        Player(10, 0, 0, 250),
        Player(14, 8, 0, 0),
        {}
    )
    spell_list = [Spell.Recharge, Spell.Shield, Spell.Drain, Spell.Poison, Spell.MagicMissile]
    backup = test_state.clone()

    print(combat(test_state, spell_list))
    print(test_state.spent)
    solve_state(backup)

tests()

input_state = State(
    Player(50, 0, 0, 500),
    Player(55, 8, 0, 0),    # from input
    {}
    )

solve_state(input_state)
