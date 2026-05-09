#!/usr/bin/env python3

class Eight(Exception):
    pass

b = 0
c = 0
d = 0
e = 0
last_e = 0
seen_numbers: set[int] = set()
while True:
    # outer loop
    c = e | 65536
    e = 521363
    while True:
        # start at 8
        d = c & 255
        e += d
        e &= 16777215
        e *= 65899
        e &= 16777215
        if 256 > c:
            break
        d = 0
        if False:
            try:
                print(f"start eight loop with {c=}")
                while True:
                    # start at 18
                    b = d + 1
                    b *= 256
                    if b > c:
                        # print(f"d is {d}")
                        c = d
                        raise Eight
                    else:
                        d += 1
            except Eight:
                # print(f"out of eight loop with {b=} {d=} {(old_c // 256)=}")
                pass
        else:
            d = c // 256
            b = (d + 1) * 256
            c = d
    # print(e)
    if e in seen_numbers:
        print(f"found loop at {e}")
        print(last_e)
        exit(0)
    seen_numbers.add(e)
    last_e = e

