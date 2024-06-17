#!/usr/bin/env python3
from math import ceil
from typing import NamedTuple
from itertools import combinations, product

Item = NamedTuple("Item", [("name", str), ("cost", int), ("damage", int), ("armor", int)])

store: dict[str, set[Item]] = {'Weapons': set(), 'Armor': set(), 'Rings': set()}

with open("21.store.txt", 'r') as f:
    shelf: str = ""
    for line in f:
        line = line.rstrip()
        if ':' in line:
            shelf = line.split(':')[0]
        elif len(line):
            stats = line.split()
            name = " ".join(stats[:-3])
            item = Item(name, int(stats[-3]), int(stats[-2]), int(stats[-1]))
            store[shelf].add(item)
# lazy version of optionality
store['Armor'].add(Item('None', 0, 0, 0))
store['Rings'].add(Item('None', 0, 0, 0))
store['Rings'].add(Item('None2', 0, 0, 0))

Player = NamedTuple("Player", [("hp", int), ("damage", int), ("armor", int)])
# lazy
boss: Player = Player(103, 9, 2)

# true if players[0] wins
def winner(players: tuple[Player, Player]) -> bool:
    hp = [p.hp for p in players]
    damage = [max(0, players[i].damage - players[1 - i].armor) for i in range(2)]
    # if a player does no damage, they will lose
    if damage[0] == 0:
        return False
    if damage[1] == 0:
        return True
    hits = [ceil(hp[1 - i] / damage[i]) for i in range(2)]
    # print (f"{hp=} {damage=} {hits=}")
    return hits[0] <= hits[1]

# print(winner((Player(8, 5, 5), Player(12, 7, 2))))

weapons_options = store['Weapons']
armor_options = store['Armor']
ring_options = combinations(store['Rings'], 2)

full_options = product(weapons_options, armor_options, ring_options)

player_hp = 100
cheapest_win: tuple[int, tuple[Item, ...]] = (1000000, ())
priciest_loss: tuple[int, tuple[Item, ...]] = (0, ())

for option in full_options:
    flat_option: tuple[Item, Item, Item, Item] = (option[0], option[1], *option[2])
    cost = sum([item.cost for item in flat_option])
    damage = sum([item.damage for item in flat_option])
    armor = sum([item.armor for item in flat_option])
    player = Player(player_hp, damage, armor)
    if winner((player, boss)):
        if cost <= cheapest_win[0]:
            cheapest_win = (cost, flat_option)
    else:
        if cost >= priciest_loss[0]:
            priciest_loss = (cost, flat_option)
print(cheapest_win)
print(priciest_loss)
