#!/usr/bin/env python3
# b = 107900
# c = 124900
b = 108100
c = b + 17000
e = 0
f = 0
h = 0
while b <= c:   # BBB loop      1001 loops
    f = 1
    d = 2
    # f is 0 if b is not prime?
    while d != b:   # AAA loop
        if b % d == 0:
            print(f"{d} factors {b}")
            f = 0
            break
        d += 1
    if f == 0:
        print(f"{b} is not prime")
        h += 1
    b += 17
print(h)
