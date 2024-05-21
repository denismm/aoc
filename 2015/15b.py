#!/usr/bin/env python3
import sys
from collections import Counter
from itertools import product

filename = sys.argv[1]

Ingredient = dict[str, int]
ingredients: dict[str, Ingredient] = {}

with open(filename, "r") as f:
    for line in f:
        line.rstrip()
        ing_name, properties = line.split(": ")
        scratch_ing: Ingredient = {}
        for prop in properties.split(", "):
            prop_name, prop_amount_s = prop.split(" ")
            scratch_ing[prop_name] = int(prop_amount_s)
        ingredients[ing_name] = scratch_ing


def score(teaspoons: dict[str, int]) -> tuple[int, int]:
    totals: Counter[str] = Counter()
    for ing_name, amount in teaspoons.items():
        # print(f"{ing_name} * {amount}")
        for prop_name, prop_amount in ingredients[ing_name].items():
            totals[prop_name] += prop_amount * amount
            # print(f"  {prop_name}: {prop_amount * amount}")
    total = 1
    # print("===")
    for prop_name, x in totals.items():
        if prop_name == "calories":
            continue
        # print(f"{prop_name} {x}")
        if x < 0:
            total = 0
        else:
            total *= x
    return (total, totals["calories"])


calorie_target = 500
# pick a starting state and search from there?
total_tsp = 100
current_amts: dict[str, int] = {}
current_score: int = 0

ing_names = list(ingredients.keys())
for amts in product(range(total_tsp + 1), repeat=len(ing_names)):
    if sum(amts) != 100:
        continue
    try_amts = {ing_name: amt for ing_name, amt in zip(ing_names, amts)}
    try_score, try_cals = score(try_amts)
    if try_cals == 500 and try_score > current_score:
        current_amts = try_amts
        current_score = try_score

print(current_score)
print(current_amts)
