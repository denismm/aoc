#!/usr/bin/env python3

import sys
number = int(sys.argv[1])

factors = [x for x in range(1, number + 1) if number % x == 0]
print(sum(factors))
