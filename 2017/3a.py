#!/usr/bin/env python3
import sys
import math

location = int(sys.argv[1])
ring = math.ceil(math.sqrt(location)) // 2
ring_start = (2 * ring - 1) ** 2
cardinal_points = [ring_start + (1 + 2 * i) * (ring) for i in range(4)]
around_dist = min( [abs(location - point) for point in cardinal_points])
# print(ring, cardinal_points, around_dist)
print(ring + around_dist)
