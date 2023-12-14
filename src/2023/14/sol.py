#!/usr/bin/env python3
import functools
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
day = 14

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

def transpose_str(g):
    return ["".join(l) for l in transpose(g)]

def tilt(g, d):
    match d:
        case "N":
            new_g = []
            for r in transpose_str(g):
                while r != (r := r.replace(".O", "O.")):
                    pass
                new_g.append(r)
            return transpose_str(new_g)
        case "S":
            new_g = []
            for r in transpose_str(g):
                while r != (r := r.replace("O.", ".O")):
                    pass
                new_g.append(r)
            return transpose_str(new_g)
        case "W":
            new_g = []
            for r in g:
                while r != (r := r.replace(".O", "O.")):
                    pass
                new_g.append(r)
            return new_g
        case "E":
            new_g = []
            for r in g:
                while r != (r := r.replace("O.", ".O")):
                    pass
                new_g.append(r)
            return new_g

def calc_load(g):
    ans = 0
    for x in range(max_x):
        for y in range(max_y):
            if g[x][y] == "O":
                ans += max_x - x
    return ans


def cycle(g):
    g = tilt(g, "N")
    g = tilt(g, "W")
    g = tilt(g, "S")
    g = tilt(g, "E")
    return g


def solve():
    # P1
    g = tilt(lines, "N")
    ans1 = calc_load(g)

    # P2
    g = lines
    seen = {}
    loops = 1000000000
    for i in range(loops):
        h = hash(tuple(g))
        if h in seen:
            start = seen[h]
            period = i - start
            loops = (loops - i) % period
            break
        seen[h] = i

        g = cycle(g)
    for i in range(loops):
        g = cycle(g)

    ans2 = calc_load(g)

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
    solve()
