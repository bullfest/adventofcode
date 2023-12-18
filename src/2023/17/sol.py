#!/usr/bin/env python3
import functools
import sys
import re
from heapq import heappop, heappush

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
day = 17


def get_d(x0, y0, x1, y1):
    if x0 < x1:
        return "E"
    if x0 > x1:
        return "W"
    if y0 < y1:
        return "S"
    if y0 > y1:
        return "N"


def solve(g, uber=False):
    visited = set()
    starts = [(0, 0, "E", 0), (0, 0, "S", 0)]
    dists = defaultdict(lambda: 100000000000)
    dists[starts[0]] = 0
    dists[starts[1]] = 0
    heap = [(0, s) for s in starts]
    while heap:
        _, n = heappop(heap)
        visited.add(n)
        x, y, d, l = n
        if x == max_x - 1 and y == max_y - 1 and (not uber or l >= 4):
            return dists[n]
        for (x1, y1) in neighbours(x, y):
            d1 = get_d(x, y, x1, y1)
            match d:
                case "E":
                    if d1 == "W":
                        continue
                case "W":
                    if d1 == "E":
                        continue
                case "N":
                    if d1 == "S":
                        continue
                case "S":
                    if d1 == "N":
                        continue
            if d == d1:
                if (uber and l == 10) or (not uber and l == 3):
                    continue
                l1 = l + 1
            else:
                if uber and l < 4:
                    continue
                l1 = 1
            n1 = (x1, y1, d1, l1)
            if n1 in visited:
                continue
            cost = dists[n] + g[x1][y1]
            if cost < dists[n1]:
                dists[n1] = cost
                heappush(heap, (cost, n1))


def run():
    global g
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
    g = get_grid(lines, int)
    flip_x_y()
    ans1 = solve(g)
    ans2 = solve(g, uber=True)
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
