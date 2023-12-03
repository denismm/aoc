#!/usr/bin/env python3
import sys
import math

location = int(sys.argv[1]) - 1
eights = math.ceil(location/8)
ring = math.floor(math.log2(eights))
ring_start = (2**ring - 1) * 8
ring_around = location - ring_start
leg_length =  ring + 1
cardinal_points = [ring_start + (1 + 2 * i) * leg_length for i in range(4)]

print(ring, cardinal_points)
