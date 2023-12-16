#!/usr/bin/env python3
import sys
import re

import aoclib
from aoclib import *
import q
import itertools as it
import math
import aocd
from typing import List, Tuple
from dataclasses import dataclass
from collections import defaultdict


def set_max_x(n: int):
    global max_x
    max_x = aoclib.max_x = n


def set_max_y(n: int):
    global max_y
    max_y = aoclib.max_y = n


def flip_x_y():
    global max_x, max_y
    max_x, max_y = max_y, max_x
    aoclib.max_x = max_x
    aoclib.max_y = max_y


year = 2023
day = 15


def HASH(s: str):
    h = 0
    for c in s:
        h += ord(c)
        h *= 17
        h %= 256
    return h


def test_HASH():
    assert HASH("HASH") == 52
    assert HASH("rn") == 0
    assert HASH("cm") == 0


def run():
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        with open(filename) as file:
            lines = [l.strip('\n') for l in file]
    else:
        filename = None
        lines = aocd.get_data(year=year, day=day).split("\n")

    print("len(lines)", len(lines))
    print("len(lines[0])", len(lines[0]))

    ans1 = 0
    ans2 = 0

    set_max_x(len(lines))
    set_max_y(len(lines[0]))

    ############
    # SOLUTION #
    ############

    instr = "".join(lines).split(",")
    for w in instr:
        ans1 += HASH(w)

    boxes = defaultdict(dict)

    for i in instr:
        if i.endswith("-"):
            w = i[:-1]
            h = HASH(i[:-1])
            boxes[h].pop(w, None)
        else:
            w, v = i.split("=")
            h = HASH(w)
            boxes[h][w] = v

    for b in boxes:
        for i, v in enumerate(boxes[b].values(), 1):
            print(b+1, i, v)
            ans2 += (b+1) * int(v) * i

    ###########
    print("1:", ans1)
    print("2:", ans2)

    if filename is None:
        submit = input("submit?")
        if 'y' in submit.lower():
            if ans1 != 0:
                aocd.submit(ans1, year=year, day=day, part="a")
            if ans2 != 0:
                aocd.submit(ans2, year=year, day=day, part="b")


if __name__ == "__main__":
    run()
