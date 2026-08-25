#!/usr/bin/env python3

import sys
from collections import Counter

width = 25
height = 6

filename = sys.argv[1]

with open(filename, 'r') as f:
    raw_data: list[int] = [int(s) for s in f.read().rstrip()]

layers: list[list[int]] = []
layer_len = width * height

for i in range(len(raw_data) // layer_len):
    layer: list[int] = raw_data[i * layer_len : (i + 1) * layer_len]
    layers.append(layer)

layer_pops: list[Counter[int]] = []
for i, layer in enumerate(layers):
    layer_pop: Counter[int] = Counter()
    for x in layer:
        layer_pop[x] += 1
    layer_pops.append(layer_pop)

layer_pops.sort(key=lambda layer_pop: layer_pop[0])
best_pop = layer_pops[0]
print(best_pop[1] * best_pop[2])

# render
final_layer: list[int] = list(layers[0])
for layer in layers[1:]:
    for pos, val in enumerate(layer):
        if final_layer[pos] == 2:
            final_layer[pos] = val

pixels = (' ', '#')
for i in range(height):
    line = final_layer[i * width : (i+1) * width]
    render: list[str] = [pixels[x] for x in line]
    print(''.join(render))
