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
day = 16


def step(m, x, y, d):
    if d == "E":
        x += 1
        if x == max_x:
            return []
        if m[x][y] == "/":
            return [(x, y, "N")]
        if m[x][y] == "\\":
            return [(x, y, "S")]
        if m[x][y] == "|":
            return [(x, y, "S"), (x, y, "N")]
        return [(x, y, "E")]
    elif d == "W":
        x -= 1
        if x == -1:
            return []
        if m[x][y] == "/":
            return [(x, y, "S")]
        if m[x][y] == "\\":
            return [(x, y, "N")]
        if m[x][y] == "|":
            return [(x, y, "S"), (x, y, "N")]
        return [(x, y, "W")]
    elif d == "N":
        y -= 1
        if y == -1:
            return []
        if m[x][y] == "/":
            return [(x, y, "E")]
        if m[x][y] == "\\":
            return [(x, y, "W")]
        if m[x][y] == "-":
            return [(x, y, "W"), (x, y, "E")]
        return [(x, y, "N")]
    elif d == "S":
        y += 1
        if y == max_y:
            return []
        if m[x][y] == "/":
            return [(x, y, "W")]
        if m[x][y] == "\\":
            return [(x, y, "E")]
        if m[x][y] == "-":
            return [(x, y, "W"), (x, y, "E")]
        return [(x, y, "S")]


def energized(m, start):
    poss = [start]
    seen = set()
    visited = set()
    while poss:
        x, y, d = poss.pop()
        if (x, y, d) in visited:
            continue
        visited.add((x, y, d))
        seen.add((x, y))
        poss += step(m, x, y, d)
    return len(seen) - 1


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
    m = get_grid(lines)
    flip_x_y()
    ans1 = energized(m, (-1, 0, "E"))
    for x in range(max_x):
        ans2 = max(ans2, energized(m, (x, -1, "S")))
        ans2 = max(ans2, energized(m, (x, max_y, "N")))
    for y in range(max_y):
        ans2 = max(ans2, energized(m, (-1, y, "E")))
        ans2 = max(ans2, energized(m, (max_x, y, "W")))
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
